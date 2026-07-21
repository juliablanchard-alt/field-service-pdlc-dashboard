#!/usr/bin/env python3
"""
WORKING Phase 0/1 refresh script - SIMPLE LOGIC ONLY
Run this after fetching MCP data and passing the result text
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

def process_mcp_result(result_text):
    """Parse MCP read_sheet_values result and extract programs"""
    programs = []

    # Parse each Row line
    for line in result_text.strip().split('\n'):
        if not line.startswith('Row '):
            continue

        try:
            # Extract row number and data
            parts = line.split(': ', 1)
            if len(parts) != 2:
                continue

            row_num_str = parts[0].replace('Row', '').strip()
            row_num = int(row_num_str)
            row_data = eval(parts[1])  # Safe - MCP output is trusted

            # Skip header rows
            if row_num < 4:
                continue

            # Extract columns (0-indexed)
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

            # SIMPLE FILTER: Must be PM Backlog, Prototyping, or Ready for Review
            if 'PM Backlog' in stage:
                phase, subcolumn = '0', 'backlog'
            elif 'Prototyping' in stage:
                phase, subcolumn = '1', 'prototyping'
            elif 'Ready for Review' in stage:
                phase, subcolumn = '1', 'ready_for_review'
            else:
                continue  # Skip this row

            # Use Feature if present, else Initiative
            name = feature.strip() if feature else initiative.strip()

            # Skip if BOTH are empty
            if not name:
                continue

            # Normalize portfolio
            if portfolio and "Field Service" not in portfolio:
                if portfolio == "Foundations":
                    portfolio = "264 Field Service Foundations"
                elif portfolio == "Mobile":
                    portfolio = "264 Field Service Mobile"
                elif "Scheduling" in portfolio or "Optimization" in portfolio:
                    portfolio = "264 Field Service Scheduling & Optimization"
                elif portfolio:
                    portfolio = f"264 Field Service {portfolio}"

            programs.append({
                "name": name,
                "full_name": name,
                "id": f"sheet_{row_num}",
                "phase": phase,
                "subcolumn": subcolumn,
                "portfolio": portfolio or "TBD",
                "stage": stage,
                "status": status,
                "program_manager": pm_lead,
                "arch_lead": arch_lead,
                "tpm_lead": tpm_lead,
                "ux_lead": ux_lead,
                "cx_lead": cx_lead,
                "health": "Unknown",
                "target_release": ""
            })

        except Exception as e:
            print(f"Warning: Could not parse row {row_num}: {e}", file=sys.stderr)
            continue

    return programs

def save_programs(programs, output_file):
    """Save programs to JSON file"""
    data = {
        "last_updated": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(),
        "source": "Google Sheets",
        "sheet_id": "1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c",
        "programs": programs
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    return True

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 refresh_phase0_WORKING.py '<mcp_result_text>'")
        print("Or pipe MCP result: echo '<result>' | python3 refresh_phase0_WORKING.py")
        return 1

    # Read from argument or stdin
    if sys.argv[1] == '-':
        result_text = sys.stdin.read()
    else:
        result_text = sys.argv[1]

    print("=" * 70)
    print("Phase 0/1 Refresh - WORKING VERSION")
    print("=" * 70)
    print()

    # Process
    programs = process_mcp_result(result_text)

    # Count
    phase_0 = [p for p in programs if p.get('phase') == '0']
    phase_1 = [p for p in programs if p.get('phase') == '1']

    print(f"📊 Parsed results:")
    print(f"   Total programs: {len(programs)}")
    print(f"   Phase 0 (PM Backlog): {len(phase_0)}")
    print(f"   Phase 1 (Prototyping/Ready): {len(phase_1)}")
    print()

    # Breakdown by portfolio
    portfolios = {}
    for p in programs:
        port = p.get('portfolio', 'TBD')
        phase = p.get('phase', '?')
        key = f"{port} (Phase {phase})"
        portfolios[key] = portfolios.get(key, 0) + 1

    print("By Portfolio:")
    for key in sorted(portfolios.keys()):
        print(f"   {key}: {portfolios[key]}")
    print()

    # Ask before saving
    response = input("Save these results? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        output_file = Path(__file__).parent / "data" / "phase_0_programs.json"
        save_programs(programs, output_file)
        print(f"✅ Saved to {output_file}")
        return 0
    else:
        print("❌ Not saved")
        return 1

if __name__ == "__main__":
    sys.exit(main())
