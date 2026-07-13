#!/usr/bin/env python3
"""
Fetch Service Cloud Execution Status data from GUS Report
Report ID: 00OEE0000032xn32AA
Shows: Programs -> Projects -> Epics with health information
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "execution_data.json"
REPORT_ID = "00OEE0000032xn32AA"

def fetch_execution_report():
    """Fetch execution report from GUS"""
    try:
        print(f"Fetching GUS report {REPORT_ID}...")
        result = subprocess.run(
            ['sf', 'api', 'request', 'rest', '--target-org', 'gus',
             f'/services/data/v64.0/analytics/reports/{REPORT_ID}',
             '--method', 'GET'],
            capture_output=True,
            text=True,
            check=True
        )

        report_data = json.loads(result.stdout)
        return report_data
    except Exception as e:
        print(f"Error fetching report: {e}")
        return None

def parse_health_from_image(html_str):
    """Extract health status from image HTML"""
    if not html_str or '-' in html_str:
        return 'Unknown'
    if 'On_Track_Green' in html_str or 'On Track' in html_str:
        return 'On Track'
    if 'Watch_Yellow' in html_str:
        return 'Watch'
    if 'Off_Track_Red' in html_str:
        return 'Blocked'
    if 'Not_Started_Gray' in html_str:
        return 'Not Started'
    return 'Unknown'

def parse_report_data(report_data):
    """Parse GUS report into structured data"""
    if not report_data:
        return {
            'last_updated': datetime.now().isoformat(),
            'programs': [],
            'summary': {}
        }

    # The report is grouped by: Program Name, Program Health, Program Health Comments
    # Data columns are: Target, Health Color, Project Name, Project Health Comments,
    #                   LOC, Epic Priority, Epic Name, Epic Health Color, Epic Health, Epic Health Comments, Last Modified

    programs_map = {}
    fact_map = report_data.get('factMap', {})

    print(f"Processing {len(fact_map)} fact map entries")

    for key, value in fact_map.items():
        if not isinstance(value, dict):
            continue

        # Parse the grouping key to get program info
        # Key format: "0!T" where 0 is the grouping level
        # The grouping values come from the key path

        # Get grouping info from the value's aggregates or from parsing the key
        # For now, let's iterate through the fact map to find program groups

        # Extract program-level data from first-level groups (keys like "0!T", "1!T", etc.)
        if '!' in key:
            parts = key.split('!')
            if len(parts[0]) <= 2:  # This is a grouping level
                # Get the grouping values
                groupings_across = value.get('aggregates', [])

                # Process rows in this group
                rows = value.get('rows', [])
                for row in rows:
                    cells = row.get('dataCells', [])

                    # Data columns (after groupings):
                    # 0: Target (Release)
                    # 1: Program Health Color (image)
                    # 2: Project Name
                    # 3: Project Health Comments
                    # 4: LOC (Theme/Bucket)
                    # 5: Epic Priority
                    # 6: Epic Name
                    # 7: Epic Health Color (image)
                    # 8: Epic Health (text)
                    # 9: Epic Health Comments
                    # 10: Last Modified Date

                    if len(cells) < 7:
                        continue

                    target_release = cells[0].get('label', '')
                    program_health_img = cells[1].get('label', '')
                    project_name = cells[2].get('label', '-')
                    project_health_comments = cells[3].get('label', '')
                    theme = cells[4].get('label', '-')
                    epic_priority = cells[5].get('label', '')
                    epic_name = cells[6].get('label', '')
                    epic_health_img = cells[7].get('label', '') if len(cells) > 7 else ''
                    epic_health_text = cells[8].get('label', '') if len(cells) > 8 else ''
                    epic_health_comments = cells[9].get('label', '') if len(cells) > 9 else ''
                    last_modified = cells[10].get('value', '') if len(cells) > 10 else ''

                    # Parse health from images
                    program_health = parse_health_from_image(program_health_img)
                    epic_health = parse_health_from_image(epic_health_img)

                    # Program info comes from the grouping - need to extract from the report extended metadata
                    # For now, use a placeholder - we'll need to map the key to the actual program name

        # Build program hierarchy
        if program_name not in programs_map:
            programs_map[program_name] = {
                'name': program_name,
                'health': program_health,
                'health_comments': program_health_comments,
                'subcloud': subcloud,
                'theme': theme,
                'target_release': target_release,
                'projects': {}
            }
        else:
            # Update health comments if we find one
            if program_health_comments and not programs_map[program_name].get('health_comments'):
                programs_map[program_name]['health_comments'] = program_health_comments

        # Only add if project name exists
        if project_name and project_name != '-':
            if project_name not in programs_map[program_name]['projects']:
                programs_map[program_name]['projects'][project_name] = {
                    'name': project_name,
                    'epics': []
                }

            if epic_name:
                programs_map[program_name]['projects'][project_name]['epics'].append({
                    'number': epic_number,
                    'name': epic_name,
                    'health': epic_health,
                    'health_status': epic_health_status,
                    'end_date': end_date
                })

    # Convert to list
    programs = []
    for prog_name, prog_data in programs_map.items():
        program = {
            'name': prog_name,
            'health': prog_data['health'],
            'health_comments': prog_data.get('health_comments', ''),
            'subcloud': prog_data['subcloud'],
            'theme': prog_data['theme'],
            'target_release': prog_data['target_release'],
            'projects': []
        }
        for proj_name, proj_data in prog_data['projects'].items():
            program['projects'].append(proj_data)
        programs.append(program)

    return {
        'last_updated': datetime.now().isoformat(),
        'programs': programs
    }

def main():
    """Main execution"""
    print("🔄 Fetching execution data from GUS...")

    report_data = fetch_execution_report()
    if not report_data:
        print("❌ Failed to fetch report")
        return 1

    parsed_data = parse_report_data(report_data)

    # Save to file
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(parsed_data, f, indent=2)

    print(f"✅ Saved {len(parsed_data['programs'])} programs to {DATA_FILE}")
    return 0

if __name__ == '__main__':
    exit(main())
