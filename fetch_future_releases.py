#!/usr/bin/env python3
"""
Fetch future release work (264 patches + 266 work) from GUS.
Discovers epics that teams are already planning for August/September and beyond.
"""

import json
import subprocess
from datetime import datetime

OUTPUT_FILE = 'data/future_releases.json'

def run_soql(query):
    """Execute SOQL query via sf CLI"""
    result = subprocess.run(
        ['sf', 'data', 'query', '--query', query, '--json', '--target-org', 'org62'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)

def fetch_future_releases():
    """
    Query GUS for 264+ patches and 266 work.
    Looking for epics with:
    - Scheduled builds in August/September (264 patches)
    - Target = 266 (Spring '27 major release)
    - Status != Canceled
    """

    print("🔍 Searching for future release work (264 patches + 266)...")

    # Query for future work
    query = """
        SELECT
            Id,
            Name,
            Team__c,
            Product_Owner__c,
            Story_Points__c,
            Scheduled_Build__c,
            Target__c,
            Priority__c,
            Health_Status__c,
            Status__c,
            Epic_Category__c,
            Program__c,
            Project__c,
            Product_Tag__r.Name,
            Planned_Release__r.Name,
            CreatedDate,
            LastModifiedDate
        FROM ADM_Epic__c
        WHERE (
            Scheduled_Build__c LIKE '%August%'
            OR Scheduled_Build__c LIKE '%September%'
            OR Scheduled_Build__c LIKE '266%'
            OR Target__c = '266'
            OR Target__c LIKE '%266%'
        )
        AND Status__c != 'Canceled'
        ORDER BY Team__c, Scheduled_Build__c
    """

    result = run_soql(query)
    records = result.get('result', {}).get('records', [])

    print(f"   Found {len(records)} epics")

    # Group by team and scheduled build
    by_team = {}
    by_release = {}

    patch_264_count = 0
    release_266_count = 0
    orphaned_count = 0

    for record in records:
        team = record.get('Team__c', 'Unknown')
        scheduled_build = record.get('Scheduled_Build__c', '-')
        target = record.get('Target__c', '-')
        story_points = record.get('Story_Points__c', 0) or 0
        program = record.get('Program__c')
        project = record.get('Project__c')

        # Categorize
        is_266 = '266' in str(target) or '266' in str(scheduled_build)
        is_patch = 'August' in str(scheduled_build) or 'September' in str(scheduled_build)
        is_orphaned = not program and not project

        if is_266:
            release_266_count += 1
        if is_patch:
            patch_264_count += 1
        if is_orphaned:
            orphaned_count += 1

        # Build epic data
        epic_data = {
            'id': record.get('Id'),
            'name': record.get('Name'),
            'team': team,
            'owner': record.get('Product_Owner__c', '-'),
            'story_points': story_points,
            'scheduled_build': scheduled_build,
            'target': target,
            'priority': record.get('Priority__c'),
            'health': record.get('Health_Status__c', '-'),
            'status': record.get('Status__c', '-'),
            'program': program or '-',
            'project': project or '-',
            'product_tag': record.get('Product_Tag__r', {}).get('Name') if record.get('Product_Tag__r') else '-',
            'planned_release': record.get('Planned_Release__r', {}).get('Name') if record.get('Planned_Release__r') else '-',
            'is_orphaned': is_orphaned,
            'category': '266 Major Release' if is_266 else '264 Patch',
            'created_date': record.get('CreatedDate', ''),
            'last_modified': record.get('LastModifiedDate', '')
        }

        # Group by team
        if team not in by_team:
            by_team[team] = {
                'team': team,
                'epics': [],
                'total_story_points': 0,
                'patch_264_points': 0,
                'release_266_points': 0,
                'orphaned_epics': 0
            }

        by_team[team]['epics'].append(epic_data)
        by_team[team]['total_story_points'] += story_points

        if is_266:
            by_team[team]['release_266_points'] += story_points
        if is_patch:
            by_team[team]['patch_264_points'] += story_points
        if is_orphaned:
            by_team[team]['orphaned_epics'] += 1

        # Group by release
        release_key = scheduled_build if scheduled_build != '-' else target
        if release_key not in by_release:
            by_release[release_key] = {
                'release': release_key,
                'epics': [],
                'total_story_points': 0,
                'teams': set()
            }

        by_release[release_key]['epics'].append(epic_data)
        by_release[release_key]['total_story_points'] += story_points
        by_release[release_key]['teams'].add(team)

    # Convert sets to lists for JSON
    for release in by_release.values():
        release['teams'] = sorted(list(release['teams']))
        release['team_count'] = len(release['teams'])

    # Sort teams by total story points
    teams_list = sorted(by_team.values(), key=lambda x: x['total_story_points'], reverse=True)
    releases_list = sorted(by_release.values(), key=lambda x: x['release'])

    # Build output
    output = {
        'last_updated': datetime.now().isoformat(),
        'summary': {
            'total_epics': len(records),
            'patch_264_epics': patch_264_count,
            'release_266_epics': release_266_count,
            'orphaned_epics': orphaned_count,
            'total_story_points': sum(r.get('Story_Points__c', 0) or 0 for r in records),
            'teams_affected': len(by_team),
            'releases_found': len(by_release)
        },
        'by_team': teams_list,
        'by_release': releases_list
    }

    # Save to file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved to {OUTPUT_FILE}")
    print(f"\n📊 Summary:")
    print(f"   Total epics: {output['summary']['total_epics']}")
    print(f"   264 patches: {patch_264_count}")
    print(f"   266 work: {release_266_count}")
    print(f"   Orphaned: {orphaned_count}")
    print(f"   Total capacity: {output['summary']['total_story_points']} story points")
    print(f"   Teams affected: {output['summary']['teams_affected']}")
    print(f"   Releases: {output['summary']['releases_found']}")

if __name__ == '__main__':
    fetch_future_releases()
