#!/usr/bin/env python3
"""
Fetch Phase 0 data from Google Sheets and update local JSON
Uses MCP Google Sheets access (requires Claude Code context)
"""

import json
import csv
import io
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1y5FS7MxqUT019bVRJuPOIH2H5Tc-8q9gH_6vXq4CMgk/edit?gid=1674131463"
SHEET_NAME = "P0 Priorites"

def parse_csv_data(csv_text):
    """Parse CSV text into program objects"""
    programs = []
    reader = csv.reader(io.StringIO(csv_text))

    # Skip first row (emoji header)
    rows = list(reader)
    if len(rows) < 2:
        print("Not enough rows in sheet")
        return []

    # Row 1 is the real header, data starts at row 2
    data_rows = rows[2:]  # Skip emoji row and header row

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
                gtm_date = datetime.strptime(row[4].strip(), "%m/%d/%Y")
                gtm_formatted = gtm_date.strftime("%b/%y")
            except:
                gtm_formatted = row[4].strip()

        # Determine prototype review month (columns 5-9)
        months = ["June", "July", "August", "September", "October"]
        review_month = None
        for i, month in enumerate(months):
            col_idx = 5 + i
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
        subcloud = prog.get("subcloud", "ZZZ")
        milestone = prog.get("next_milestone", "")
        month_rank = 999
        for month, rank in month_order.items():
            if month in milestone:
                month_rank = rank
                break
        return (subcloud, month_rank)

    programs.sort(key=sort_key)
    return programs

def save_programs(programs):
    """Save programs to JSON file with timestamp"""
    try:
        pt_time = datetime.now(ZoneInfo("America/Los_Angeles"))
        data = {
            "last_updated": pt_time.isoformat(),
            "programs": programs
        }

        JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Successfully synced {len(programs)} Phase 0 programs")
        for prog in programs:
            print(f"   - {prog['name']} (PM: {prog['pm']})")
        return True
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")
        return False

def main():
    """Main function - expects CSV data from stdin"""
    print("📊 Fetching Phase 0 data from Google Sheets...")

    # Read CSV data from stdin (piped from MCP tool)
    csv_data = sys.stdin.read()

    if not csv_data:
        print("❌ No data received")
        return 1

    programs = parse_csv_data(csv_data)

    if programs:
        success = save_programs(programs)
        return 0 if success else 1
    else:
        print("❌ No programs found in sheet")
        return 1

if __name__ == "__main__":
    sys.exit(main())
