#!/usr/bin/env python3
"""
Update Phase 0 data from Google Sheets - Run via Claude Code
This file can be called by you saying: "Run update_phase0_now.py"
"""

import json
from pathlib import Path
from datetime import datetime

# This will be filled in by Claude Code when you ask to update
SHEET_DATA_ROWS = []

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"

# Column mapping
COL_PORTFOLIO = 0
COL_STAGE = 3
COL_FEATURE = 8
COL_STATUS = 16
COL_PM_LEAD = 17
COL_ARCH_LEAD = 18
COL_TPM_LEAD = 19
COL_UX_LEAD = 20
COL_CX_LEAD = 21

def parse_sheet_rows(rows):
    """Parse rows into programs"""
    programs = []

    # Find header
    header_idx = None
    for i, row in enumerate(rows):
        if row and 'Portfolio' in str(row[0]):
            header_idx = i
            break

    if header_idx is None:
        return []

    # Parse data
    for row in rows[header_idx + 1:]:
        if not row or len(row) < 9:
            continue

        portfolio = row[COL_PORTFOLIO] if len(row) > COL_PORTFOLIO else ''
        stage = row[COL_STAGE] if len(row) > COL_STAGE else ''
        feature = row[COL_FEATURE] if len(row) > COL_FEATURE else ''

        if not feature or not portfolio or 'Engineering Backlog' in str(stage):
            continue

        # Determine phase
        phase = '0'
        if 'Discovery' in str(stage) or 'Phase 1' in str(stage) or 'Prototyping' in str(stage) or 'Approved' in str(stage):
            phase = '1'

        programs.append({
            'name': str(feature)[:80],
            'portfolio': str(portfolio),
            'stage': str(stage),
            'phase': phase,
            'status': str(row[COL_STATUS]) if len(row) > COL_STATUS else '',
            'pm_lead': str(row[COL_PM_LEAD]) if len(row) > COL_PM_LEAD else '',
            'arch_lead': str(row[COL_ARCH_LEAD]) if len(row) > COL_ARCH_LEAD else '',
            'tpm_lead': str(row[COL_TPM_LEAD]) if len(row) > COL_TPM_LEAD else '',
            'ux_lead': str(row[COL_UX_LEAD]) if len(row) > COL_UX_LEAD else '',
            'cx_lead': str(row[COL_CX_LEAD]) if len(row) > COL_CX_LEAD else '',
        })

    return programs

def update_from_rows(rows):
    """Update JSON file from sheet rows"""
    programs = parse_sheet_rows(rows)

    data = {
        'last_updated': datetime.now().isoformat(),
        'source': 'Google Sheets',
        'sheet_id': '1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c',
        'programs': programs
    }

    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    phase_0 = sum(1 for p in programs if p['phase'] == '0')
    phase_1 = sum(1 for p in programs if p['phase'] == '1')

    print(f"✅ Updated {len(programs)} programs")
    print(f"   Phase 0: {phase_0}")
    print(f"   Phase 1: {phase_1}")
    print(f"   File: {JSON_FILE}")

    return {
        'total': len(programs),
        'phase_0': phase_0,
        'phase_1': phase_1
    }

if __name__ == '__main__':
    # For testing - Claude Code will call update_from_rows() directly
    if SHEET_DATA_ROWS:
        update_from_rows(SHEET_DATA_ROWS)
    else:
        print("❌ No sheet data provided")
        print("   Ask Claude Code to: 'Update Phase 0 data from Google Sheets'")
