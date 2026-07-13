#!/usr/bin/env python3
"""
Run REAL PBD validation for all Phase 1 programs
This must be run from within Claude Code to access the /validate-pbd skill
"""

import json
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "validation_reports"
JSON_FILE = SCRIPT_DIR / "data" / "phase_1_programs.json"

# PBDs to validate
PBDS = [
    {
        "id": "1eOfq7snNp5qJxqA06ApmAo2cRwtS9tdjbsaIn1y_hNI",
        "name": "Case Classification AI",
        "url": "https://docs.google.com/document/d/1eOfq7snNp5qJxqA06ApmAo2cRwtS9tdjbsaIn1y_hNI/edit",
        "pm": "David Kim",
        "arch": "Michael Torres"
    },
    {
        "id": "1L1SniCWC_f7wpdDs0HS8h-mkM1ho7Xc0AjvRcBiSNz0",
        "name": "Industry Compliance Tracker",
        "url": "https://docs.google.com/document/d/1L1SniCWC_f7wpdDs0HS8h-mkM1ho7Xc0AjvRcBiSNz0/edit",
        "pm": "Maria Santos",
        "arch": "Amit Patel"
    },
    {
        "id": "1O2ZV03Cj9Y2my_AhSmqcHNdoOVm8vTz6i7I-X-H_rvA",
        "name": "Commerce Personalization Engine",
        "url": "https://docs.google.com/document/d/1O2ZV03Cj9Y2my_AhSmqcHNdoOVm8vTz6i7I-X-H_rvA/edit",
        "pm": "Alex Rodriguez",
        "arch": "Sarah Kim"
    },
    {
        "id": "1IsrkySrHQgZoG0w2cJO-OnRfQA878XVamNUb67vqonM",
        "name": "Loyalty Insights Dashboard",
        "url": "https://docs.google.com/document/d/1IsrkySrHQgZoG0w2cJO-OnRfQA878XVamNUb67vqonM/edit",
        "pm": "Kira Bauer",
        "arch": "James Lee"
    },
    {
        "id": "1G9qlJ30thewnZDrLEMFQ3QL5H89wytC_t3W95-OF8oI",
        "name": "Service Agent Copilot",
        "url": "https://docs.google.com/document/d/1G9qlJ30thewnZDrLEMFQ3QL5H89wytC_t3W95-OF8oI/edit",
        "pm": "Sarah Chen",
        "arch": "Priya Singh"
    }
]

def main():
    """
    This script should be called from Claude Code with instructions to:
    1. For each PBD, run: /validate-pbd <url>
    2. Save the markdown report to validation_reports/<program_name>.md
    3. Parse the report to extract status and completion
    4. Update phase_1_programs.json with real validation data
    """

    print("=" * 60)
    print("REAL PBD VALIDATION - Instructions for Claude Code")
    print("=" * 60)
    print()
    print("Please run the following commands in Claude Code:")
    print()

    REPORTS_DIR.mkdir(exist_ok=True)

    for i, pbd in enumerate(PBDS, 1):
        report_file = REPORTS_DIR / f"{pbd['name'].replace(' ', '_')}.md"
        print(f"{i}. /validate-pbd {pbd['url']}")
        print(f"   Save report to: {report_file}")
        print()

    print("After running all validations, the reports will be in:")
    print(f"  {REPORTS_DIR}/")
    print()
    print("Then run: python3 parse_validation_reports.py")
    print("To update the dashboard with real validation data")
    print("=" * 60)

if __name__ == "__main__":
    main()
