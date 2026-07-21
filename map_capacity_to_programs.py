#!/usr/bin/env python3
"""
Map team capacity (delivered/committed) to specific programs
by tracing work items through Epic -> Project -> Program hierarchy
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

# Query June delivered work items with epic/project info
print("\n🔄 Mapping June delivered capacity to programs...")
team_ids_str = "', '".join(team_ids)
june_query = f"""
SELECT Id, Name, Scrum_Team__c, Story_Points__c, Epic__r.Name, Epic__r.Project__r.Name
FROM ADM_Work__c
WHERE First_Time_In_Progress__c >= 2026-06-01T00:00:00Z
  AND Closed_On__c >= 2026-06-01T00:00:00Z
  AND Closed_On__c < 2026-07-01T00:00:00Z
  AND Scrum_Team__c IN ('{team_ids_str}')
  AND Story_Points__c != null
LIMIT 50000
"""

june_items = run_soql(june_query)
print(f"✅ Found {len(june_items)} June work items")

# Aggregate by team + program
june_team_program = defaultdict(lambda: defaultdict(float))
june_unmapped = defaultdict(float)

for item in june_items:
    team_id = item.get('Scrum_Team__c')
    points = item.get('Story_Points__c', 0) or 0

    epic = item.get('Epic__r')
    project = epic.get('Project__r') if epic else None
    project_name = project.get('Name') if project else None

    if team_id in team_name_map:
        team_name = team_name_map[team_id]

        if project_name and project_name in project_to_program:
            program_name = project_to_program[project_name]
            june_team_program[team_name][program_name] += points
        elif not project_name:
            # Only count as unmapped if there's NO project at all
            june_unmapped[team_name] += points
        # else: has project but not in program map - don't count as unmapped

# Query July committed work items
print("\n🔄 Mapping July committed capacity to programs...")
july_query = f"""
SELECT Id, Name, Scrum_Team__c, Story_Points__c, Epic__r.Name, Epic__r.Project__r.Name
FROM ADM_Work__c
WHERE Sprint_Timeframe__c LIKE '2026.07%'
  AND Scrum_Team__c IN ('{team_ids_str}')
  AND Story_Points__c != null
  AND Status__c NOT IN ('Closed', 'Never', 'Cancelled', 'Duplicate')
LIMIT 50000
"""

july_items = run_soql(july_query)
print(f"✅ Found {len(july_items)} July work items")

july_team_program = defaultdict(lambda: defaultdict(float))
july_unmapped = defaultdict(float)

for item in july_items:
    team_id = item.get('Scrum_Team__c')
    points = item.get('Story_Points__c', 0) or 0

    epic = item.get('Epic__r')
    project = epic.get('Project__r') if epic else None
    project_name = project.get('Name') if project else None

    if team_id in team_name_map:
        team_name = team_name_map[team_id]

        if project_name and project_name in project_to_program:
            program_name = project_to_program[project_name]
            july_team_program[team_name][program_name] += points
        elif not project_name:
            # Only count as unmapped if there's NO project at all
            july_unmapped[team_name] += points
        # else: has project but not in program map - don't count as unmapped

# Update teams data with program breakdown
for team in teams_data['teams']:
    team_name = team['name']

    # June delivered by program
    team['june_delivered_by_program'] = dict(june_team_program.get(team_name, {}))
    team['june_delivered_unmapped'] = june_unmapped.get(team_name, 0)

    # July committed by program
    team['july_committed_by_program'] = dict(july_team_program.get(team_name, {}))
    team['july_committed_unmapped'] = july_unmapped.get(team_name, 0)

# Save updated data
with open(TEAMS_FILE, 'w') as f:
    json.dump(teams_data, f, indent=2)

# Print summary
print("\n📊 June Delivered Capacity by Program:")
june_program_totals = defaultdict(float)
for team_name, programs in june_team_program.items():
    for program, points in programs.items():
        june_program_totals[program] += points

for program, points in sorted(june_program_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {program}: {points:.1f} points")

total_june_unmapped = sum(june_unmapped.values())
print(f"  [Unmapped]: {total_june_unmapped:.1f} points")

print("\n📊 July Committed Capacity by Program:")
july_program_totals = defaultdict(float)
for team_name, programs in july_team_program.items():
    for program, points in programs.items():
        july_program_totals[program] += points

for program, points in sorted(july_program_totals.items(), key=lambda x: x[1], reverse=True):
    print(f"  {program}: {points:.1f} points")

total_july_unmapped = sum(july_unmapped.values())
print(f"  [Unmapped]: {total_july_unmapped:.1f} points")

print(f"\n✅ Updated {TEAMS_FILE}")
