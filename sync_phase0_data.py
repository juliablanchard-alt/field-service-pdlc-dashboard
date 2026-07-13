#!/usr/bin/env python3
"""
Sync Phase 0 Dashboard Data from Google Sheet

Fetches data from "266 DE Priorites" Google Sheet and updates the local JSON file.
Designed to be run via Claude Code with MCP Google access.
"""

import json
import csv
import io
from pathlib import Path

# File paths
SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"

def parse_csv_to_programs(csv_data):
    """Parse CSV data into program objects"""
    if not csv_data:
        print("No CSV data provided")
        return []

    programs = []
    reader = csv.reader(io.StringIO(csv_data))

    # Convert to list and skip first 2 rows (header rows)
    rows = list(reader)
    if len(rows) < 3:
        print("Not enough rows in sheet")
        return []

    data_rows = rows[2:]  # Skip header rows

    for row in data_rows:
        if len(row) < 12:  # Need at least 12 columns
            continue

        initiative = row[2].strip()
        if not initiative:  # Skip empty rows
            continue

        # Extract data
        subcloud = row[0].strip() if len(row) > 0 and row[0] else "TBD"
        pm_lead = row[11].strip() if len(row) > 11 and row[11] else "TBD"
        arch_lead = row[12].strip() if len(row) > 12 and row[12] else "TBD"

        # Parse GTM date (column 4) and format as Month/YY
        gtm_formatted = "TBD"
        if len(row) > 4 and row[4]:
            try:
                from datetime import datetime
                gtm_date = datetime.strptime(row[4].strip(), "%m/%d/%Y")
                gtm_formatted = gtm_date.strftime("%b/%y")
            except:
                gtm_formatted = row[4].strip()

        # Determine prototype review month
        months = ["June", "July", "August", "September", "October"]
        review_month = None
        for i, month in enumerate(months):
            col_idx = 5 + i  # Columns 5-9 are the month flags (shifted due to GTM column)
            if len(row) > col_idx and row[col_idx].upper() == "TRUE":
                review_month = month
                break

        program = {
            "name": initiative,
            "pm": pm_lead,
            "arch": arch_lead,
            "subcloud": subcloud,
            "gtm": gtm_formatted,
            "completion": 0,
            "next_milestone": f"Prototype Review - {review_month}" if review_month else "TBD"
        }
        programs.append(program)

    # Sort by subcloud, then by prototype review month
    month_order = {"June": 1, "July": 2, "August": 3, "September": 4, "October": 5}

    def sort_key(prog):
        subcloud = prog.get("subcloud", "ZZZ")  # Put TBD at the end
        milestone = prog.get("next_milestone", "")

        # Extract month from "Prototype Review - {Month}"
        month_rank = 999  # Default for TBD or unparseable
        for month, rank in month_order.items():
            if month in milestone:
                month_rank = rank
                break

        return (subcloud, month_rank)

    programs.sort(key=sort_key)

    return programs

def save_programs(programs):
    """Save programs to JSON file"""
    try:
        from datetime import datetime
        from zoneinfo import ZoneInfo

        # Add timestamp in Pacific Time
        pt_time = datetime.now(ZoneInfo("America/Los_Angeles"))
        data = {
            "last_updated": pt_time.isoformat(),
            "programs": programs
        }

        JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Successfully synced {len(programs)} programs to {JSON_FILE}")
        for prog in programs:
            print(f"   - {prog['name']} (PM: {prog['pm']}, Arch: {prog['arch']})")
        return True

    except Exception as e:
        print(f"Error writing JSON file: {e}")
        return False

if __name__ == "__main__":
    # This script expects CSV data to be piped in or provided as first argument
    import sys
    if len(sys.argv) > 1:
        csv_data = sys.argv[1]
    else:
        csv_data = sys.stdin.read()

    programs = parse_csv_to_programs(csv_data)
    if programs:
        success = save_programs(programs)
        sys.exit(0 if success else 1)
    else:
        print("No programs to sync")
        sys.exit(1)
