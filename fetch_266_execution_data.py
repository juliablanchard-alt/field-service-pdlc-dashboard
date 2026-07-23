#!/usr/bin/env python3
"""
Fetch 266 Field Service Execution data via SOQL query.
Discovers Phase 2+ programs in 266 portfolios and structures them like 264 data.
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "execution_266_data.json"
TARGET_ORG = os.getenv("TARGET_ORG", "org62")

def run_soql(query):
    """Execute SOQL query via sf CLI"""
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

def fetch_266_programs():
    """
    Query for 266 programs that are Phase 2 or beyond.
    Phase 2 = Build & Test (actively being developed)
    """
    print("🔍 Querying for 266 programs at Phase 2+...")

    # Query programs with 266 in Product_Tag__c and Phase >= 2
    # Note: Phase__c values are picklist: "0 - Ideation", "1 - Prototyping", "2 - Build & Test", "3 - Launch & Iterate"
    query = """
        SELECT Id, Name, Product_Tag__r.Name, Phase__c,
               Product_Owner__r.Name, Health__c, Health_Comments__c,
               LastModifiedDate, CreatedDate
        FROM ADM_Product_Request__c
        WHERE Product_Tag__r.Name LIKE '266%'
          AND (Phase__c = '2 - Build & Test' OR Phase__c = '3 - Launch & Iterate')
        ORDER BY Product_Tag__r.Name, Name
    """

    programs = run_soql(query)
    print(f"✅ Found {len(programs)} programs in 266 portfolios at Phase 2+")
    return programs

def fetch_projects_for_programs(program_ids):
    """Query projects that belong to these programs"""
    if not program_ids:
        return []

    print(f"🔍 Querying projects for {len(program_ids)} programs...")

    # Batch query
    BATCH_SIZE = 100
    all_projects = []

    for i in range(0, len(program_ids), BATCH_SIZE):
        batch = program_ids[i:i+BATCH_SIZE]
        ids_str = "', '".join(batch)

        query = f"""
            SELECT Id, Name, Program__c,
                   Product_Owner__r.Name, Health__c, Health_Comments__c,
                   LastModifiedDate, CreatedDate
            FROM ADM_Project__c
            WHERE Program__c IN ('{ids_str}')
            ORDER BY Name
        """

        projects = run_soql(query)
        all_projects.extend(projects)

    print(f"✅ Found {len(all_projects)} projects")
    return all_projects

def fetch_epics_for_projects(project_ids):
    """Query epics that belong to these projects"""
    if not project_ids:
        return []

    print(f"🔍 Querying epics for {len(project_ids)} projects...")

    # Batch query
    BATCH_SIZE = 100
    all_epics = []

    for i in range(0, len(project_ids), BATCH_SIZE):
        batch = project_ids[i:i+BATCH_SIZE]
        ids_str = "', '".join(batch)

        query = f"""
            SELECT Id, Name, Project__c,
                   Priority__c, Health__c, Epic_Health_Comments__c,
                   Owner.Name, Team__r.Name,
                   Scheduled_Build__r.Name, Planned_Release__r.Name,
                   Actual_Story_Points_on_Epic__c,
                   Path_to_Green__c, LOC__c, Pillar__c,
                   LastModifiedDate, CreatedDate
            FROM ADM_Epic__c
            WHERE Project__c IN ('{ids_str}')
              AND Health__c NOT IN ('Completed', 'Canceled')
            ORDER BY Project__c, Name
        """

        epics = run_soql(query)
        all_epics.extend(epics)

    print(f"✅ Found {len(all_epics)} epics")
    return all_epics

def structure_266_data(programs, projects, epics):
    """Structure 266 data in same format as execution_data.json"""

    # Group projects by program
    projects_by_program = defaultdict(list)
    for project in projects:
        program_id = project.get('Program__c')
        if program_id:
            projects_by_program[program_id].append(project)

    # Group epics by project
    epics_by_project = defaultdict(list)
    for epic in epics:
        project_id = epic.get('Project__c')
        if project_id:
            epics_by_project[project_id].append(epic)

    # Build program structure
    programs_list = []

    for program in programs:
        program_id = program.get('Id')
        portfolio = program.get('Product_Tag__r', {}).get('Name', '266') if program.get('Product_Tag__r') else '266'

        # Build projects for this program
        projects_list = []
        for project in projects_by_program.get(program_id, []):
            project_id = project.get('Id')

            # Build epics for this project
            epics_list = []
            for epic in epics_by_project.get(project_id, []):
                owner_obj = epic.get('Owner')
                team_obj = epic.get('Team__r')
                scheduled_build_obj = epic.get('Scheduled_Build__r')
                planned_release_obj = epic.get('Planned_Release__r')

                epic_data = {
                    'id': epic.get('Id', ''),
                    'name': epic.get('Name', ''),
                    'priority': epic.get('Priority__c', '-'),
                    'health': epic.get('Health__c', 'Unknown'),
                    'health_comments': epic.get('Epic_Health_Comments__c', '-'),
                    'owner': owner_obj.get('Name', '-') if owner_obj else '-',
                    'team': team_obj.get('Name', '-') if team_obj else '-',
                    'scheduled_build': scheduled_build_obj.get('Name', '-') if scheduled_build_obj else '-',
                    'planned_release': planned_release_obj.get('Name', '-') if planned_release_obj else '-',
                    'story_points': epic.get('Actual_Story_Points_on_Epic__c', 0) or 0,
                    'path_to_green': epic.get('Path_to_Green__c', '-'),
                    'loc': epic.get('LOC__c', '-'),
                    'pillar': epic.get('Pillar__c', '-'),
                    'last_modified': epic.get('LastModifiedDate', '')[:10] if epic.get('LastModifiedDate') else '',
                }

                epics_list.append(epic_data)

            # Build project data
            product_owner_obj = project.get('Product_Owner__r')
            project_data = {
                'id': project.get('Id', ''),
                'name': project.get('Name', ''),
                'product_owner': product_owner_obj.get('Name', '-') if product_owner_obj else '-',
                'health': project.get('Health__c', 'Unknown'),
                'health_comments': project.get('Health_Comments__c', '-'),
                'epics': epics_list,
                'epic_count': len(epics_list),
                'total_story_points': sum(e['story_points'] for e in epics_list),
            }

            projects_list.append(project_data)

        # Build program data
        product_owner_obj = program.get('Product_Owner__r')
        program_data = {
            'id': program_id,
            'name': program.get('Name', ''),
            'portfolio': portfolio,
            'phase': program.get('Phase__c', 'Unknown'),
            'product_owner': product_owner_obj.get('Name', '-') if product_owner_obj else '-',
            'health': program.get('Health__c', 'Unknown'),
            'health_comments': program.get('Health_Comments__c', '-'),
            'projects': projects_list,
            'project_count': len(projects_list),
            'epic_count': sum(p['epic_count'] for p in projects_list),
            'total_story_points': sum(p['total_story_points'] for p in projects_list),
        }

        programs_list.append(program_data)

    return {
        'last_updated': datetime.now().isoformat(),
        'source': '266 Phase 2+ SOQL Query',
        'programs': programs_list,
        'summary': {
            'total_programs': len(programs_list),
            'total_projects': sum(p['project_count'] for p in programs_list),
            'total_epics': sum(p['epic_count'] for p in programs_list),
            'total_story_points': sum(p['total_story_points'] for p in programs_list),
        }
    }

def main():
    print("=" * 60)
    print("Fetching 266 Field Service Execution Data")
    print("=" * 60)

    # Step 1: Get 266 programs at Phase 2+
    programs = fetch_266_programs()

    if not programs:
        print("\n⚠️  No 266 programs found at Phase 2+")
        # Save empty structure
        empty_data = {
            'last_updated': datetime.now().isoformat(),
            'source': '266 Phase 2+ SOQL Query',
            'programs': [],
            'summary': {
                'total_programs': 0,
                'total_projects': 0,
                'total_epics': 0,
                'total_story_points': 0,
            }
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(empty_data, f, indent=2)
        print(f"\n✅ Saved empty structure to {DATA_FILE}")
        return

    # Step 2: Get projects for these programs
    program_ids = [p.get('Id') for p in programs if p.get('Id')]
    projects = fetch_projects_for_programs(program_ids)

    # Step 3: Get epics for these projects
    project_ids = [p.get('Id') for p in projects if p.get('Id')]
    epics = fetch_epics_for_projects(project_ids)

    # Step 4: Structure the data
    structured_data = structure_266_data(programs, projects, epics)

    # Step 5: Save to file
    with open(DATA_FILE, 'w') as f:
        json.dump(structured_data, f, indent=2)

    print(f"\n✅ Saved to {DATA_FILE}")
    print(f"\n📊 Summary:")
    print(f"   Programs: {structured_data['summary']['total_programs']}")
    print(f"   Projects: {structured_data['summary']['total_projects']}")
    print(f"   Epics: {structured_data['summary']['total_epics']}")
    print(f"   Total Capacity: {structured_data['summary']['total_story_points']} PD")

    # List unique portfolios discovered
    portfolios = set(p['portfolio'] for p in structured_data['programs'])
    print(f"\n📦 Portfolios discovered:")
    for portfolio in sorted(portfolios):
        count = sum(1 for p in structured_data['programs'] if p['portfolio'] == portfolio)
        print(f"   - {portfolio}: {count} programs")

if __name__ == '__main__':
    main()
