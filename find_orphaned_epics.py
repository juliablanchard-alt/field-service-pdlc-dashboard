#!/usr/bin/env python3
"""
Find truly orphaned Field Service epics - those with no program or project
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "orphaned_epics.json"
TARGET_ORG = "org62"

def sf_data_query(query):
    """Execute SOQL query using sf data query command"""
    try:
        result = subprocess.run(
            ['sf', 'data', 'query', '--target-org', TARGET_ORG,
             '--query', query, '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data.get('result', {}).get('records', [])
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

def find_orphaned_epics():
    """
    Find Field Service epics that are missing program OR project assignments
    """
    query = """
    SELECT Id, Name, Health__c, Epic_Health_Comments__c,
           Priority__c, Scheduled_Build__r.Name,
           Owner.Name, Team__r.Name,
           PPM_Project__c, PPM_Program__c,
           Status__c, Last_Modified_Date,
           Actual_Story_Points_on_Epic__c
    FROM ADM_Epic__c
    WHERE (Team__r.Name LIKE '%Field Service%'
           OR Team__r.Name LIKE '%SFS%'
           OR Team__r.Name LIKE '%FSL%')
      AND Status__c NOT IN ('Completed', 'Released', 'Canceled')
      AND (PPM_Program__c = null OR PPM_Project__c = null)
    ORDER BY Team__r.Name, Last_Modified_Date DESC
    """

    print("Querying for orphaned Field Service epics...")
    records = sf_data_query(query)
    print(f"Found {len(records)} orphaned epics")

    return records

def parse_orphaned_epics(records):
    """Parse orphaned epic records"""
    epics = []

    for record in records:
        # Parse story points
        try:
            story_points = float(record.get('Actual_Story_Points_on_Epic__c', 0) or 0)
        except:
            story_points = 0

        epic = {
            'id': record.get('Id', ''),
            'name': record.get('Name', ''),
            'priority': record.get('Priority__c', '-'),
            'health': record.get('Health__c', 'Unknown'),
            'health_comments': record.get('Epic_Health_Comments__c', '-'),
            'owner': record.get('Owner', {}).get('Name', '-') if record.get('Owner') else '-',
            'team': record.get('Team__r', {}).get('Name', '-') if record.get('Team__r') else '-',
            'scheduled_build': record.get('Scheduled_Build__r', {}).get('Name', '-') if record.get('Scheduled_Build__r') else '-',
            'status': record.get('Status__c', 'Unknown'),
            'last_modified': record.get('Last_Modified_Date', '')[:10] if record.get('Last_Modified_Date') else '',
            'story_points': story_points,
            'has_project': bool(record.get('PPM_Project__c')),
            'has_program': bool(record.get('PPM_Program__c'))
        }

        epics.append(epic)

    return epics

def main():
    """Main execution flow"""
    print("=" * 60)
    print("Finding Orphaned Field Service Epics")
    print("=" * 60)

    # Find orphaned epics
    records = find_orphaned_epics()

    if not records:
        print("\n✅ No orphaned epics found! All epics have programs/projects.")
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_orphaned': 0,
            'total_capacity': 0,
            'by_team': [],
            'epics': []
        }
    else:
        # Parse records
        epics = parse_orphaned_epics(records)

        # Calculate stats
        total_capacity = sum(e['story_points'] for e in epics)
        no_project = sum(1 for e in epics if not e['has_project'])
        no_program = sum(1 for e in epics if not e['has_program'])

        # Group by team
        from collections import defaultdict
        teams = defaultdict(list)
        for epic in epics:
            teams[epic['team']].append(epic)

        by_team = [
            {
                'name': team_name,
                'epic_count': len(team_epics),
                'total_capacity': sum(e['story_points'] for e in team_epics),
                'epics': team_epics
            }
            for team_name, team_epics in sorted(teams.items())
        ]

        output = {
            'last_updated': datetime.now().isoformat(),
            'total_orphaned': len(epics),
            'no_project': no_project,
            'no_program': no_program,
            'total_capacity': round(total_capacity, 1),
            'by_team': by_team,
            'epics': epics
        }

        print(f"\n⚠️ Found {len(epics)} orphaned epics")
        print(f"  Missing Project: {no_project}")
        print(f"  Missing Program: {no_program}")
        print(f"  Total Capacity: {round(total_capacity, 1)} PD")
        print(f"\nBy Team:")
        for team in by_team:
            print(f"  {team['name']}: {team['epic_count']} epics ({team['total_capacity']} PD)")

    # Save to file
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved to {DATA_FILE}")

if __name__ == '__main__':
    main()
