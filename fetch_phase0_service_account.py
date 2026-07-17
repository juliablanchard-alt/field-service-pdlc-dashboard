#!/usr/bin/env python3
"""
Fetch Phase 0 & Phase 1 data from Google Sheets using Service Account credentials
This script can run in GitHub Actions or locally with proper credentials
Includes: PM Backlog (Phase 0), Prototyping (Phase 1 Col 1), Ready for Review (Phase 1 Col 2)
"""

import json
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SPREADSHEET_ID = "1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c"
SHEET_NAME = "Phase 0 & Phase 1 Priorites"
RANGE_NAME = f"'{SHEET_NAME}'!A1:Z1000"

# Service account credentials can be provided via:
# 1. Environment variable GOOGLE_SERVICE_ACCOUNT_JSON (JSON string)
# 2. File path in environment variable GOOGLE_APPLICATION_CREDENTIALS
# 3. File at ./credentials/service-account.json

def get_sheets_service():
    """Get authenticated Google Sheets API service"""
    if not GOOGLE_LIBS_AVAILABLE:
        raise Exception("Google API libraries not installed. Run: pip install google-api-python-client google-auth")

    credentials = None

    # Try environment variable with JSON content
    if 'GOOGLE_SERVICE_ACCOUNT_JSON' in os.environ:
        service_account_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        print("✅ Using credentials from GOOGLE_SERVICE_ACCOUNT_JSON environment variable")

    # Try environment variable with file path
    elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        credentials = service_account.Credentials.from_service_account_file(
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        print(f"✅ Using credentials from {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")

    # Try default location
    else:
        creds_file = SCRIPT_DIR / "credentials" / "service-account.json"
        if creds_file.exists():
            credentials = service_account.Credentials.from_service_account_file(
                str(creds_file),
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            print(f"✅ Using credentials from {creds_file}")
        else:
            raise Exception(
                "No service account credentials found. Please provide credentials via:\n"
                "  1. GOOGLE_SERVICE_ACCOUNT_JSON environment variable, or\n"
                "  2. GOOGLE_APPLICATION_CREDENTIALS environment variable, or\n"
                "  3. ./credentials/service-account.json file"
            )

    service = build('sheets', 'v4', credentials=credentials)
    return service

def fetch_sheet_data():
    """Fetch data from Google Sheet using Service Account"""
    try:
        print(f"🔄 Fetching data from Google Sheet...")
        print(f"   Spreadsheet ID: {SPREADSHEET_ID}")
        print(f"   Range: {RANGE_NAME}")

        service = get_sheets_service()
        sheet = service.spreadsheets()

        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get('values', [])

        if not values:
            print("❌ No data found in sheet")
            return None

        print(f"✅ Retrieved {len(values)} rows from Google Sheet")
        return values

    except Exception as e:
        print(f"❌ Error fetching Google Sheet: {e}")
        return None

def parse_sheet_data(values):
    """Parse Google Sheets data"""
    programs = []

    for row_num, row_data in enumerate(values, start=1):
        # Skip header rows (1-3)
        if row_num < 4:
            continue

        try:
            if len(row_data) < 9:
                continue

            portfolio = row_data[0] if len(row_data) > 0 else ""
            stage = row_data[3] if len(row_data) > 3 else ""
            initiative = row_data[4] if len(row_data) > 4 else ""
            feature = row_data[8] if len(row_data) > 8 else ""
            status = row_data[16] if len(row_data) > 16 else ""
            pm_lead = row_data[17] if len(row_data) > 17 else ""
            arch_lead = row_data[18] if len(row_data) > 18 else ""
            tpm_lead = row_data[19] if len(row_data) > 19 else ""
            ux_lead = row_data[20] if len(row_data) > 20 else ""
            cx_lead = row_data[21] if len(row_data) > 21 else ""

            # Use Initiative as fallback if Feature is empty
            display_name = feature if feature else initiative

            # Only include Phase 0 and Phase 1 items (PM Backlog, Prototyping, Ready for Review)
            # Must have either a Feature or Initiative
            if not display_name or ("PM Backlog" not in stage and "Prototyping" not in stage and "Ready for Review" not in stage):
                continue

            # Normalize portfolio name
            if portfolio and "Field Service" not in portfolio:
                if portfolio == "Foundations":
                    portfolio = "264 Field Service Foundations"
                elif portfolio == "Mobile":
                    portfolio = "264 Field Service Mobile"
                elif portfolio == "Workforce Scheduling":
                    portfolio = "264 Field Service Workforce Scheduling"
                elif "Scheduling" in portfolio:
                    portfolio = "264 Field Service Scheduling & Optimization"
                elif portfolio:
                    portfolio = f"264 Field Service {portfolio}"

            # Determine phase and subcolumn based on stage
            if "PM Backlog" in stage:
                phase = "0"
                subcolumn = "backlog"
            elif "Prototyping" in stage:
                phase = "1"
                subcolumn = "prototyping"
            elif "Ready for Review" in stage:
                phase = "1"
                subcolumn = "ready_for_review"
            else:
                phase = "0"
                subcolumn = "backlog"

            program = {
                "name": display_name,
                "full_name": display_name,
                "id": f"sheet_{row_num}",
                "phase": phase,
                "subcolumn": subcolumn,
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

        except Exception as e:
            print(f"Warning: Could not parse row {row_num}: {e}")
            continue

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

        print(f"✅ Saved {len(programs)} Phase 0 & Phase 1 programs to {JSON_FILE}")

        # Group by portfolio for summary
        by_portfolio = {}
        for p in programs:
            portfolio = p.get("portfolio", "TBD")
            by_portfolio[portfolio] = by_portfolio.get(portfolio, 0) + 1

        print("\nPrograms by portfolio:")
        for portfolio in sorted(by_portfolio.keys()):
            print(f"   {portfolio}: {by_portfolio[portfolio]}")

        return True
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Phase 0 & Phase 1 Google Sheet Refresh (Service Account)")
    print("=" * 60)

    values = fetch_sheet_data()

    if not values:
        return 1

    programs = parse_sheet_data(values)

    if programs:
        success = save_programs(programs)
        return 0 if success else 1
    else:
        print("❌ No Phase 0 & Phase 1 programs found in sheet")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
