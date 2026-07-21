#!/usr/bin/env python3
"""
Check orphaned epics to see if all their work items are closed/nevered.
Identifies epics that are functionally complete but status not updated.
"""

import json
import subprocess
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ORPHANED_FILE = SCRIPT_DIR / "data" / "unallocated_data.json"
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

print("Loading orphaned epics...")
with open(ORPHANED_FILE, 'r') as f:
    orphaned_data = json.load(f)

orphaned_epics = [e for e in orphaned_data['epics'] if e.get('is_orphaned')]
epic_ids = [e['id'] for e in orphaned_epics]

print(f"Found {len(epic_ids)} orphaned epics")
print(f"Querying work items for these epics...")

# Query work items in batches
batch_size = 100
all_complete_epics = []
epic_work_summary = {}

for i in range(0, len(epic_ids), batch_size):
    batch = epic_ids[i:i+batch_size]
    ids_str = "', '".join(batch)
    
    query = f"""
    SELECT Id, Epic__c, Status__c
    FROM ADM_Work__c
    WHERE Epic__c IN ('{ids_str}')
    """
    
    work_items = run_soql(query)
    
    # Group by epic
    epic_work = defaultdict(list)
    for item in work_items:
        epic_id = item.get('Epic__c')
        status = item.get('Status__c', 'Unknown')
        epic_work[epic_id].append(status)
    
    # Check which epics have all work in terminal states
    terminal_states = {'Closed', 'Never', 'Cancelled', 'Duplicate'}
    
    for epic_id in batch:
        work_statuses = epic_work.get(epic_id, [])
        
        if not work_statuses:
            # No work items found
            epic_work_summary[epic_id] = {'total': 0, 'closed': 0, 'all_closed': False}
        else:
            closed_count = sum(1 for s in work_statuses if s in terminal_states)
            all_closed = closed_count == len(work_statuses)
            
            epic_work_summary[epic_id] = {
                'total': len(work_statuses),
                'closed': closed_count,
                'all_closed': all_closed
            }
            
            if all_closed:
                all_complete_epics.append(epic_id)
    
    print(f"  Processed {min(i+batch_size, len(epic_ids))}/{len(epic_ids)} epics...")

print(f"\n✅ Analysis complete")
print(f"\nEpics with ALL work items closed/nevered: {len(all_complete_epics)}")

# Show details
complete_epics_detail = []
for epic in orphaned_epics:
    if epic['id'] in all_complete_epics:
        work = epic_work_summary[epic['id']]
        complete_epics_detail.append({
            'id': epic['id'],
            'name': epic['name'],
            'team': epic['team'],
            'health': epic['health'],
            'story_points': epic['story_points'],
            'work_items_total': work['total'],
            'scheduled_build': epic['scheduled_build']
        })

if complete_epics_detail:
    total_capacity = sum(e['story_points'] for e in complete_epics_detail)
    print(f"Total capacity: {total_capacity:.0f} PD")
    print(f"\nTop 20 epics by capacity:")
    for epic in sorted(complete_epics_detail, key=lambda x: x['story_points'] or 0, reverse=True)[:20]:
        sp = epic['story_points'] or 0
        health = epic['health'] or 'Unknown'
        print(f"  {sp:>6.0f} PD | {health:<12} | {epic['team']:<40} | {epic['name'][:60]}")

# Epics with NO work items at all
no_work_epics = [e for e in orphaned_epics if epic_work_summary.get(e['id'], {}).get('total', 0) == 0]
no_work_capacity = sum(e['story_points'] for e in no_work_epics)
print(f"\n\nEpics with NO work items: {len(no_work_epics)} ({no_work_capacity:.0f} PD)")

# Save results
output = {
    'all_closed': complete_epics_detail,
    'no_work': [{'id': e['id'], 'name': e['name'], 'team': e['team'], 'story_points': e['story_points']} for e in no_work_epics]
}

output_file = SCRIPT_DIR / "data" / "epic_work_status.json"
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Saved results to {output_file}")
