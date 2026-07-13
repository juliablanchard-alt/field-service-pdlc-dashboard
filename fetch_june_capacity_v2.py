#!/usr/bin/env python3
"""
Fetch work items completed in June 2026 by Field Service teams
Calculate capacity delivered (story points) per team
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "teams_data.json"
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

# Step 1: Get all Field Service scrum team IDs
print("🔄 Fetching Field Service scrum teams...")
teams_query = """
SELECT Id, Name
FROM ADM_Scrum_Team__c
WHERE Name LIKE 'FSL -%'
   OR Name LIKE 'SFS %'
   OR Name = 'MomentumForce'
   OR Name = 'QuantumForce'
   OR Name = 'SynergyForce'
   OR Name = 'Optimization Engineering'
"""
scrum_teams = run_soql(teams_query)
team_name_map = {team['Id']: team['Name'] for team in scrum_teams}
team_ids = list(team_name_map.keys())

print(f"✅ Found {len(scrum_teams)} Field Service scrum teams")

# Step 2: Query work items closed in June 2026 for these teams
print(f"🔄 Querying work items closed in June 2026...")

# Build WHERE clause with team IDs
team_ids_str = "', '".join(team_ids[:100])  # Limit to 100 teams to avoid query size limits
work_query = f"""
SELECT Id, Name, Scrum_Team__c, Story_Points__c, Closed_On__c, Status__c
FROM ADM_Work__c
WHERE Closed_On__c >= 2026-06-01T00:00:00Z
  AND Closed_On__c < 2026-07-01T00:00:00Z
  AND Scrum_Team__c IN ('{team_ids_str}')
  AND Story_Points__c != null
LIMIT 50000
"""

work_items = run_soql(work_query)
print(f"✅ Found {len(work_items)} work items with story points closed in June 2026")

# Step 3: Aggregate by team
team_capacity = defaultdict(lambda: {'points': 0, 'work_items': 0})

for item in work_items:
    team_id = item.get('Scrum_Team__c')
    story_points = item.get('Story_Points__c', 0) or 0

    if team_id in team_name_map:
        team_name = team_name_map[team_id]
        team_capacity[team_name]['points'] += story_points
        team_capacity[team_name]['work_items'] += 1

# Step 4: Load existing teams data and update with capacity
with open(DATA_FILE, 'r') as f:
    teams_data = json.load(f)

for team in teams_data['teams']:
    team_name = team['name']
    if team_name in team_capacity:
        team['capacity_delivered_june'] = round(team_capacity[team_name]['points'], 1)
        team['work_items_closed_june'] = team_capacity[team_name]['work_items']
    else:
        team['capacity_delivered_june'] = 0
        team['work_items_closed_june'] = 0

# Save updated data
with open(DATA_FILE, 'w') as f:
    json.dump(teams_data, f, indent=2)

# Print summary
print(f"\n📊 Capacity Delivered - June 2026:")
print(f"{'Team':<50} {'Story Points':>15} {'Work Items':>12}")
print("=" * 80)

total_points = 0
total_items = 0

for team in sorted(teams_data['teams'], key=lambda t: t.get('capacity_delivered_june', 0), reverse=True):
    points = team.get('capacity_delivered_june', 0)
    items = team.get('work_items_closed_june', 0)
    if points > 0 or items > 0:
        print(f"{team['name']:<50} {points:>15.1f} {items:>12}")
        total_points += points
        total_items += items

print("=" * 80)
print(f"{'TOTAL':<50} {total_points:>15.1f} {total_items:>12}")

print(f"\n✅ Updated {DATA_FILE}")
