#!/usr/bin/env python3
"""
Fetch Field Service Execution data - CORRECTED to properly parse hierarchy
Report structure: Portfolio → Program → Project → Epic
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "execution_data.json"
REPORT_ID = "00OEE000002tswH2AQ"
TARGET_ORG = "org62"

def fetch_report():
    """Fetch report from GUS"""
    result = subprocess.run(
        ['sf', 'api', 'request', 'rest', '--target-org', TARGET_ORG,
         f'/services/data/v64.0/analytics/reports/{REPORT_ID}?includeDetails=true',
         '--method', 'GET'],
        capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)

def parse_health(health_str):
    """Extract health status from string"""
    if not health_str or health_str == '-':
        return 'Unknown'
    h = health_str.lower()
    if 'on track' in h: return 'On Track'
    if 'watch' in h: return 'Watch'
    if 'blocked' in h: return 'Blocked'
    if 'not started' in h: return 'Not Started'
    if 'completed' in h or 'complete' in h: return 'Completed'
    return 'Unknown'

print("🔄 Fetching execution data from GUS...")
report_data = fetch_report()

programs_map = {}

# Hierarchy: Portfolio (level 1) → Program (level 2) → Project (level 3) → Epic (detail rows)
portfolios = report_data.get('groupingsDown', {}).get('groupings', [])

for portfolio in portfolios:
    portfolio_name = portfolio.get('label', 'Unknown')

    # Level 2: Programs
    for program_group in portfolio.get('groupings', []):
        program_name = program_group.get('label', 'Unknown')
        program_id = program_group.get('value', '')

        if program_name not in programs_map:
            programs_map[program_name] = {
                'name': program_name,
                'id': program_id,
                'portfolio': portfolio_name,
                'health': 'Unknown',
                'program_manager': '',
                'projects': {}
            }

        # Level 3: Projects
        for project_group in program_group.get('groupings', []):
            project_name = project_group.get('label', 'Unknown')

            if project_name not in programs_map[program_name]['projects']:
                programs_map[program_name]['projects'][project_name] = {
                    'name': project_name,
                    'epics': []
                }

            # Get epic detail rows
            fact_key = project_group.get('key', '') + '!T'
            fact_data = report_data.get('factMap', {}).get(fact_key, {})
            rows = fact_data.get('rows', [])

            for row in rows:
                cells = row.get('dataCells', [])
                if len(cells) < 5:
                    continue

                epic_name = cells[0].get('label', '')
                epic_health = parse_health(cells[4].get('label', ''))
                program_health = parse_health(cells[14].get('label', '')) if len(cells) > 14 else 'Unknown'

                # Update program health from first epic
                if programs_map[program_name]['health'] == 'Unknown':
                    programs_map[program_name]['health'] = program_health

                if epic_name:
                    programs_map[program_name]['projects'][project_name]['epics'].append({
                        'name': epic_name,
                        'health': epic_health,
                        'health_status': epic_health
                    })

# Convert to list
programs_list = []
for prog_name, prog_data in programs_map.items():
    prog_data['projects'] = list(prog_data['projects'].values())
    programs_list.append(prog_data)

output = {
    'last_updated': datetime.now().isoformat(),
    'programs': programs_list
}

DATA_FILE.write_text(json.dumps(output, indent=2))
print(f"✅ Saved {len(programs_list)} programs to {DATA_FILE}")

# Show summary
total_projects = sum(len(p['projects']) for p in programs_list)
total_epics = sum(sum(len(proj['epics']) for proj in p['projects']) for p in programs_list)
print(f"   Programs: {len(programs_list)}")
print(f"   Projects: {total_projects}")
print(f"   Epics: {total_epics}")
