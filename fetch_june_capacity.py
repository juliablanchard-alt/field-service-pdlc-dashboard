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

# Field Service team names from the roster report
FS_TEAMS = [
    'FSL - Asset - 360',
    'FSL - Core - Foundations',
    'FSL - Foundation - Apps',
    'FSL - Foundation - Atlas',
    'FSL - Foundation - Corecodiles',
    'FSL - Operations - Intelligence',
    'FSL - Resource - Dispatch Console',
    'FSL - Resource - Scheduling Hawks',
    'FSL - Resource - Scheduling Intelligence',
    'FSL - Resource - Scheduling Orcas',
    'FSL - Resource - Scheduling Platform',
    'MomentumForce',
    'Optimization Engineering',
    'QuantumForce',
    'SFS Core Scheduler',
    'SFS Frontline AI',
    'SFS Mobile AGX',
    'SFS Mobile Assets',
    'SFS Mobile Comms and Search',
    'SFS Mobile Core Experience',
    'SFS Mobile Location and DC',
    'SFS Mobile Offline Extensibility',
    'SFS Mobile Platform DX',
    'SFS Mobile - Quality',
    'SFS Mobile Services',
    'SFS Setup Experience',
    'SFS - WFM - Worker - Experience',
    'SynergyForce'
]

def run_soql(query):
    """Execute SOQL query"""
    result = subprocess.run(
        ['sf', 'data', 'query', '--target-org', TARGET_ORG,
         '--query', query, '--json'],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout)
    return data.get('result', {}).get('records', [])

print("🔄 Querying work items closed in June 2026...")

# Query work items closed in June 2026 with story points
# Using Closed_On__c for completion date
query = """
SELECT Id, Name, Scrum_Team__r.Name, Story_Points__c, Closed_On__c,
       Status__c, Subject__c
FROM ADM_Work__c
WHERE Closed_On__c >= 2026-06-01T00:00:00Z
  AND Closed_On__c < 2026-07-01T00:00:00Z
  AND Scrum_Team__c != null
  AND Story_Points__c != null
ORDER BY Scrum_Team__r.Name, Closed_On__c
"""

work_items = run_soql(query)
print(f"✅ Found {len(work_items)} work items with story points closed in June 2026")

# Aggregate by team
team_capacity = defaultdict(lambda: {'points': 0, 'work_items': 0})

for item in work_items:
    team_name = item.get('Scrum_Team__r', {}).get('Name', 'Unknown')
    story_points = item.get('Story_Points__c', 0) or 0

    # Only track Field Service teams
    if team_name in FS_TEAMS:
        team_capacity[team_name]['points'] += story_points
        team_capacity[team_name]['work_items'] += 1

# Load existing teams data and update with capacity
with open(DATA_FILE, 'r') as f:
    teams_data = json.load(f)

for team in teams_data['teams']:
    team_name = team['name']
    if team_name in team_capacity:
        team['capacity_delivered_june'] = team_capacity[team_name]['points']
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
    if points > 0:
        print(f"{team['name']:<50} {points:>15.1f} {items:>12}")
        total_points += points
        total_items += items

print("=" * 80)
print(f"{'TOTAL':<50} {total_points:>15.1f} {total_items:>12}")

print(f"\n✅ Updated {DATA_FILE}")
