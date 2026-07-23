#!/usr/bin/env python3
"""
Populate August and September capacity by querying work items with
Scheduled_Build__c containing August/September patches or 266 releases
"""

import json
import subprocess
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
TEAMS_FILE = SCRIPT_DIR / "data" / "teams_data.json"
EXECUTION_FILE = SCRIPT_DIR / "data" / "execution_data.json"
TARGET_ORG = "org62"

def run_soql(query):
    """Execute SOQL query"""
    result = subprocess.run(
        ['sf', 'data', 'query', '--target-org', TARGET_ORG,
         '--query', query, '--json'],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout)
    return data.get('result', {}).get('records', [])

# Load execution data to get program-project mappings
print("🔄 Loading execution data...")
with open(EXECUTION_FILE, 'r') as f:
    execution_data = json.load(f)

# Build project -> program mapping
project_to_program = {}
for program in execution_data.get('programs', []):
    if not program.get('portfolio', '').startswith('264'):
        continue
    program_name = program.get('name', '')
    for project in program.get('projects', []):
        project_name = project.get('name', '')
        project_to_program[project_name] = program_name

print(f"✅ Mapped {len(project_to_program)} projects to programs")

# Load teams data
print("🔄 Loading teams data...")
with open(TEAMS_FILE, 'r') as f:
    teams_data = json.load(f)

active_team_names = [team['name'] for team in teams_data['teams']]

# Get scrum team IDs
print("🔄 Fetching scrum team IDs...")
name_conditions = " OR ".join([f"Name = '{name}'" for name in active_team_names])
teams_query = f"""
SELECT Id, Name
FROM ADM_Scrum_Team__c
WHERE {name_conditions}
"""
scrum_teams = run_soql(teams_query)
team_name_map = {team['Id']: team['Name'] for team in scrum_teams}
team_ids = list(team_name_map.keys())
print(f"✅ Found {len(scrum_teams)} teams")

team_ids_str = "', '".join(team_ids)

# Query August epics first (264.2 patch)
print("\n🔄 Finding August epics (264.2 patch)...")
august_epics_query = f"""
SELECT Id, Name, Scheduled_Build__r.Name, Project__r.Name
FROM ADM_Epic__c
WHERE Scheduled_Build__r.Name IN ('264.2')
LIMIT 5000
"""

august_epics = run_soql(august_epics_query)
august_epic_ids = [e['Id'] for e in august_epics]
august_epic_to_project = {e['Id']: e.get('Project__r', {}).get('Name') if e.get('Project__r') else None for e in august_epics}

print(f"✅ Found {len(august_epics)} August epics")

# Query work items for these epics (batch if needed due to query length limits)
august_items = []
if august_epic_ids:
    BATCH_SIZE = 100  # Salesforce query length limit
    for i in range(0, len(august_epic_ids), BATCH_SIZE):
        batch = august_epic_ids[i:i+BATCH_SIZE]
        august_epic_ids_str = "', '".join(batch)
        august_query = f"""
        SELECT Id, Name, Scrum_Team__c, Story_Points__c, Epic__c
        FROM ADM_Work__c
        WHERE Epic__c IN ('{august_epic_ids_str}')
          AND Scrum_Team__c IN ('{team_ids_str}')
          AND Story_Points__c != null
        LIMIT 50000
        """
        batch_items = run_soql(august_query)
        august_items.extend(batch_items)
    print(f"✅ Found {len(august_items)} August work items")

# Aggregate by team + program
august_team_program = defaultdict(lambda: defaultdict(float))
august_unmapped = defaultdict(float)

for item in august_items:
    team_id = item.get('Scrum_Team__c')
    points = item.get('Story_Points__c', 0) or 0
    epic_id = item.get('Epic__c')

    project_name = august_epic_to_project.get(epic_id)

    if team_id in team_name_map:
        team_name = team_name_map[team_id]

        if project_name and project_name in project_to_program:
            program_name = project_to_program[project_name]
            august_team_program[team_name][program_name] += points
        elif not project_name:
            # Unmapped (no project assignment)
            august_unmapped[team_name] += points

# Query September epics (264.3 patch + early 266)
print("\n🔄 Finding September epics (264.3 patch + 266 work)...")
september_epics_query = f"""
SELECT Id, Name, Scheduled_Build__r.Name, Project__r.Name
FROM ADM_Epic__c
WHERE Scheduled_Build__r.Name IN ('264.3', '266', '266.0', '266.1')
LIMIT 5000
"""

september_epics = run_soql(september_epics_query)
september_epic_ids = [e['Id'] for e in september_epics]
september_epic_to_project = {e['Id']: e.get('Project__r', {}).get('Name') if e.get('Project__r') else None for e in september_epics}

print(f"✅ Found {len(september_epics)} September epics")

# Query work items for these epics (batch if needed due to query length limits)
september_items = []
if september_epic_ids:
    BATCH_SIZE = 100  # Salesforce query length limit
    for i in range(0, len(september_epic_ids), BATCH_SIZE):
        batch = september_epic_ids[i:i+BATCH_SIZE]
        september_epic_ids_str = "', '".join(batch)
        september_query = f"""
        SELECT Id, Name, Scrum_Team__c, Story_Points__c, Epic__c
        FROM ADM_Work__c
        WHERE Epic__c IN ('{september_epic_ids_str}')
          AND Scrum_Team__c IN ('{team_ids_str}')
          AND Story_Points__c != null
        LIMIT 50000
        """
        batch_items = run_soql(september_query)
        september_items.extend(batch_items)
        print(f"   Batch {i//BATCH_SIZE + 1}: {len(batch_items)} items")
    print(f"✅ Found {len(september_items)} September work items total")

september_team_program = defaultdict(lambda: defaultdict(float))
september_unmapped = defaultdict(float)

for item in september_items:
    team_id = item.get('Scrum_Team__c')
    points = item.get('Story_Points__c', 0) or 0
    epic_id = item.get('Epic__c')

    project_name = september_epic_to_project.get(epic_id)

    if team_id in team_name_map:
        team_name = team_name_map[team_id]

        if project_name and project_name in project_to_program:
            program_name = project_to_program[project_name]
            september_team_program[team_name][program_name] += points
        elif not project_name:
            # Unmapped (no project assignment)
            september_unmapped[team_name] += points

# Update teams data with program breakdown
for team in teams_data['teams']:
    team_name = team['name']

    # August committed by program
    august_by_prog = dict(august_team_program.get(team_name, {}))
    august_unmapped_val = august_unmapped.get(team_name, 0)

    team['august_committed_by_program'] = august_by_prog
    team['august_committed_unmapped'] = august_unmapped_val
    team['capacity_committed_august'] = sum(august_by_prog.values()) + august_unmapped_val
    team['work_items_committed_august'] = len([i for i in august_items if team_name_map.get(i.get('Scrum_Team__c')) == team_name])

    # September committed by program
    september_by_prog = dict(september_team_program.get(team_name, {}))
    september_unmapped_val = september_unmapped.get(team_name, 0)

    team['september_committed_by_program'] = september_by_prog
    team['september_committed_unmapped'] = september_unmapped_val
    team['capacity_committed_september'] = sum(september_by_prog.values()) + september_unmapped_val
    team['work_items_committed_september'] = len([i for i in september_items if team_name_map.get(i.get('Scrum_Team__c')) == team_name])

# Save updated data
with open(TEAMS_FILE, 'w') as f:
    json.dump(teams_data, f, indent=2)

# Print summary
print("\n📊 August Committed Capacity by Program:")
august_program_totals = defaultdict(float)
for team_name, programs in august_team_program.items():
    for program, points in programs.items():
        august_program_totals[program] += points

for program, points in sorted(august_program_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {program}: {points:.1f} points")

total_august_unmapped = sum(august_unmapped.values())
print(f"  [Unmapped]: {total_august_unmapped:.1f} points")

print("\n📊 September Committed Capacity by Program:")
september_program_totals = defaultdict(float)
for team_name, programs in september_team_program.items():
    for program, points in programs.items():
        september_program_totals[program] += points

for program, points in sorted(september_program_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {program}: {points:.1f} points")

total_september_unmapped = sum(september_unmapped.values())
print(f"  [Unmapped]: {total_september_unmapped:.1f} points")

print(f"\n✅ Updated {TEAMS_FILE}")
