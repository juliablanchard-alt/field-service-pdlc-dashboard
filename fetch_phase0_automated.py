#!/usr/bin/env python3
"""
Automated Phase 0 data fetcher using Google Workspace MCP via subprocess
Can be run by cron or manually - uses Claude Code's MCP tools
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SHEET_ID = "1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c"
SHEET_RANGE = "'Phase 0 & Phase 1 Priorites'!A1:Z1000"

# Column mapping (0-indexed)
COL_PORTFOLIO = 0      # A
COL_STAGE = 3          # D
COL_FEATURE = 8        # I
COL_STATUS = 16        # Q
COL_PM_LEAD = 17       # R
COL_ARCH_LEAD = 18     # S
COL_TPM_LEAD = 19      # T
COL_UX_LEAD = 20       # U
COL_CX_LEAD = 21       # V

def fetch_sheet_via_claude_mcp():
    """Fetch Google Sheet using Claude Code MCP server"""
    print("🔄 Fetching Phase 0 data from Google Sheet...")
    print(f"   Sheet ID: {SHEET_ID}")
    print(f"   Range: {SHEET_RANGE}")

    try:
        # Use claude-code CLI to call MCP tool
        # This assumes claude-code is in PATH and MCP server is configured
        cmd = [
            'claude-code', 'mcp', 'call',
            'google-workspace-readonly',
            'read_sheet_values',
            '--spreadsheet_id', SHEET_ID,
            '--range_name', SHEET_RANGE
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ MCP call failed: {result.stderr}")
            return None

        # Parse the output - should be JSON
        try:
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError:
            print(f"❌ Could not parse MCP response as JSON")
            print(f"   Raw output: {result.stdout[:200]}")
            return None

    except FileNotFoundError:
        print("❌ claude-code CLI not found")
        print("   Make sure Claude Code is installed and in your PATH")
        return None
    except subprocess.TimeoutExpired:
        print("❌ Timeout fetching Google Sheet (60s)")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def parse_sheet_rows(rows):
    """Parse raw sheet rows into program data"""
    programs = []

    # Find header row (should be row with 'Portfolio' in first column)
    header_idx = None
    for i, row in enumerate(rows):
        if row and len(row) > 0 and row[0] == 'Portfolio':
            header_idx = i
            break

    if header_idx is None:
        print("❌ Could not find header row with 'Portfolio'")
        return []

    print(f"✓ Found header at row {header_idx + 1}")

    # Parse data rows
    for i, row in enumerate(rows[header_idx + 1:], start=header_idx + 2):
        if not row or len(row) < 9:  # Need at least Feature column
            continue

        portfolio = row[COL_PORTFOLIO] if len(row) > COL_PORTFOLIO else ''
        stage = row[COL_STAGE] if len(row) > COL_STAGE else ''
        feature = row[COL_FEATURE] if len(row) > COL_FEATURE else ''

        # Skip empty rows
        if not feature or not portfolio:
            continue

        # Skip engineering backlog items (not programs)
        if 'Engineering Backlog' in stage:
            continue

        # Determine phase based on stage
        phase = '0'
        if 'PM Backlog' in stage or 'Phase 0' in stage:
            phase = '0'
        elif 'Discovery' in stage or 'Phase 1' in stage:
            phase = '1'

        program = {
            'name': feature[:80],  # Truncate long names
            'portfolio': portfolio,
            'stage': stage,
            'phase': phase,
            'status': row[COL_STATUS] if len(row) > COL_STATUS else '',
            'pm_lead': row[COL_PM_LEAD] if len(row) > COL_PM_LEAD else '',
            'arch_lead': row[COL_ARCH_LEAD] if len(row) > COL_ARCH_LEAD else '',
            'tpm_lead': row[COL_TPM_LEAD] if len(row) > COL_TPM_LEAD else '',
            'ux_lead': row[COL_UX_LEAD] if len(row) > COL_UX_LEAD else '',
            'cx_lead': row[COL_CX_LEAD] if len(row) > COL_CX_LEAD else '',
        }

        programs.append(program)

    return programs

def save_programs(programs):
    """Save programs to JSON file"""
    data = {
        'last_updated': datetime.now().isoformat(),
        'source': 'Google Sheets',
        'sheet_id': SHEET_ID,
        'programs': programs
    }

    # Ensure data directory exists
    JSON_FILE.parent.mkdir(exist_ok=True)

    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved {len(programs)} programs to {JSON_FILE}")

    # Stats
    phase_0 = sum(1 for p in programs if p['phase'] == '0')
    phase_1 = sum(1 for p in programs if p['phase'] == '1')
    print(f"   Phase 0: {phase_0}, Phase 1: {phase_1}")

def main():
    """Main entry point"""
    sheet_data = fetch_sheet_via_claude_mcp()

    if not sheet_data:
        print("❌ Failed to fetch sheet data")
        sys.exit(1)

    # Extract rows from MCP response
    # The MCP tool returns a formatted string, we need to parse it
    # For now, let's use a simpler approach - write to temp file and parse
    print("❌ Direct MCP parsing not yet implemented")
    print("   Please use the manual process for now")
    sys.exit(1)

if __name__ == '__main__':
    main()
