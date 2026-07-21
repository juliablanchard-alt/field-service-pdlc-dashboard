#!/usr/bin/env python3
"""
Check orphaned epics to see which are owned by inactive employees.
"""

import json
import subprocess
from pathlib import Path
from collections import Counter

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
print(f"Found {len(orphaned_epics)} orphaned epics")

# Get unique owner names
owners = set(e['owner'] for e in orphaned_epics if e.get('owner') and e['owner'] != '-')
print(f"Found {len(owners)} unique owners")

# Query User records to check IsActive status
print("Checking owner active status...")
owner_names = list(owners)
batch_size = 50
inactive_owners = set()
active_owners = set()

for i in range(0, len(owner_names), batch_size):
    batch = owner_names[i:i+batch_size]
    names_str = "', '".join(batch)
    
    query = f"""
    SELECT Name, IsActive
    FROM User
    WHERE Name IN ('{names_str}')
    """
    
    users = run_soql(query)
    
    for user in users:
        name = user.get('Name')
        is_active = user.get('IsActive', True)
        
        if is_active:
            active_owners.add(name)
        else:
            inactive_owners.add(name)
    
    print(f"  Checked {min(i+batch_size, len(owner_names))}/{len(owner_names)} owners...")

print(f"\n✅ Owner analysis complete")
print(f"Active owners: {len(active_owners)}")
print(f"Inactive owners: {len(inactive_owners)}")

if inactive_owners:
    print(f"\nInactive owners:")
    for owner in sorted(inactive_owners):
        epics = [e for e in orphaned_epics if e.get('owner') == owner]
        capacity = sum(e['story_points'] for e in epics)
        print(f"  {owner}: {len(epics)} epics, {capacity:.0f} PD")

# Epics owned by inactive employees
inactive_epics = [e for e in orphaned_epics if e.get('owner') in inactive_owners]
inactive_capacity = sum(e['story_points'] for e in inactive_epics)

print(f"\n\nTOTAL epics owned by inactive employees: {len(inactive_epics)} ({inactive_capacity:.0f} PD)")

# Save results
output = {
    'inactive_owners': list(inactive_owners),
    'inactive_owned_epics': [
        {
            'id': e['id'],
            'name': e['name'],
            'owner': e['owner'],
            'team': e['team'],
            'story_points': e['story_points'],
            'health': e['health']
        }
        for e in inactive_epics
    ]
}

output_file = SCRIPT_DIR / "data" / "inactive_owner_epics.json"
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ Saved results to {output_file}")
