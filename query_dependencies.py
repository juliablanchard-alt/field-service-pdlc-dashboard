#!/usr/bin/env python3
"""Query dependencies for epics"""
import subprocess
import json
import sys

# Query dependencies
query = """
SELECT Id, Name, Epic__r.Name, Dependent_Team__c, Dependency_Type__c, Status__c, Notes__c
FROM ADM_Team_Dependency__c 
WHERE Epic__r.Planned_Release__r.Name LIKE '%264%'
"""

result = subprocess.run(
    ['sf', 'data', 'query', '--query', query, '--target-org', 'org62', '--json'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
records = data.get('result', {}).get('records', [])

print(f"Found {len(records)} dependencies")

# Group by epic
by_epic = {}
for rec in records:
    epic_name = rec.get('Epic__r', {}).get('Name', 'Unknown')
    if epic_name not in by_epic:
        by_epic[epic_name] = []
    by_epic[epic_name].append(rec)

print(f"\nDependencies by epic:")
for epic, deps in sorted(by_epic.items()):
    print(f"  {epic}: {len(deps)} dependencies")
