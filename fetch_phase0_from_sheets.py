#!/usr/bin/env python3
"""
Fetch Phase 0 data from Field Service Google Sheet
Uses sf org command to fetch via Google Sheets API
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SPREADSHEET_ID = "1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c"
SHEET_NAME = "Phase 0 & Phase 1 Priorites"

def fetch_sheet_data():
    """Fetch data from Google Sheet using sf CLI"""
    try:
        # Use sf data query to get Google Sheets data via Connected App
        # This is a placeholder - need to implement actual Google Sheets API call
        print(f"📊 Fetching Phase 0 data from Google Sheet {SPREADSHEET_ID}...")

        # For now, return None to indicate we need a different approach
        return None
    except Exception as e:
        print(f"❌ Error fetching sheet data: {e}")
        return None

def parse_sheet_rows(rows):
    """Parse Google Sheet rows into Phase 0 program objects"""
    programs = []

    # Expected columns from "Phase 0 & Phase 1 Priorites" sheet:
    # A=Portfolio, D=Stage, I=Feature, Q=Status, R=PM Lead, S=Arch Lead, T=TPM Lead, U=UX Lead, V=CX Lead

    for i, row in enumerate(rows):
        if i < 3:  # Skip header rows
            continue

        if len(row) < 9:  # Need at least feature name (column I = index 8)
            continue

        portfolio = row[0] if len(row) > 0 else ""
        stage = row[3] if len(row) > 3 else ""
        feature = row[8] if len(row) > 8 else ""
        status = row[16] if len(row) > 16 else ""
        pm_lead = row[17] if len(row) > 17 else ""
        arch_lead = row[18] if len(row) > 18 else ""
        tpm_lead = row[19] if len(row) > 19 else ""
        ux_lead = row[20] if len(row) > 20 else ""
        cx_lead = row[21] if len(row) > 21 else ""

        # Only include Phase 0 items (PM Backlog)
        if not feature or "PM Backlog" not in stage:
            continue

        # Normalize portfolio name
        if portfolio and "Field Service" not in portfolio:
            portfolio = f"264 Field Service {portfolio}"

        program = {
            "name": feature,
            "full_name": feature,
            "id": f"sheet_{i}",
            "phase": "0",
            "subcolumn": "backlog",
            "portfolio": portfolio or "TBD",
            "stage": stage,
            "status": status or "",
            "program_manager": pm_lead or "",
            "arch_lead": arch_lead or "",
            "tpm_lead": tpm_lead or "",
            "ux_lead": ux_lead or "",
            "cx_lead": cx_lead or "",
            "health": "Unknown",
            "target_release": ""
        }
        programs.append(program)

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

        print(f"✅ Saved {len(programs)} Phase 0 programs to {JSON_FILE}")
        return True
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")
        return False

def main():
    """Main function"""
    print("🔄 Fetching Phase 0 data from Field Service Google Sheet...")
    print(f"   Sheet ID: {SPREADSHEET_ID}")
    print(f"   Sheet: {SHEET_NAME}")
    print()
    print("⚠️  This script requires manual execution via Claude Code with MCP Google Sheets access")
    print("   Run: Tell Claude to fetch Phase 0 data and save to phase_0_programs.json")
    return 1

if __name__ == "__main__":
    sys.exit(main())
