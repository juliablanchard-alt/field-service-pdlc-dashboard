#!/usr/bin/env python3
"""Build complete static dashboard with all 5 portfolios"""
import json
import sys
from datetime import datetime
from collections import defaultdict

# Load all data
with open('data/execution_data.json', 'r') as f:
    execution_data = json.load(f)
with open('data/phase_0_programs.json', 'r') as f:
    phase_0_data = json.load(f)
with open('data/phase_1_programs.json', 'r') as f:
    phase_1_data = json.load(f)
with open('data/teams_data.json', 'r') as f:
    teams_data = json.load(f)
with open('templates/field_service_dynamic.html', 'r') as f:
    template = f.read()

# Extract CSS
css_start = template.find('<style>') + 7
css_end = template.find('</style>')
css = template[css_start:css_end]

# Get ALL Field Service portfolios (don't hardcode - match Flask logic)
all_exec_portfolios = set(p.get('portfolio') for p in execution_data.get('programs', []) if p.get('portfolio') and ('Field Service' in p.get('portfolio', '') or 'UWM' in p.get('portfolio', '')))
all_phase0_portfolios = set(p.get('portfolio') for p in phase_0_data.get('programs', []) if p.get('portfolio') and ('Field Service' in p.get('portfolio', '') or 'UWM' in p.get('portfolio', '')))
all_phase1_portfolios = set(p.get('portfolio') for p in phase_1_data.get('programs', []) if p.get('portfolio') and ('Field Service' in p.get('portfolio', '') or 'UWM' in p.get('portfolio', '')))

FS_PORTFOLIOS = sorted(all_exec_portfolios | all_phase0_portfolios | all_phase1_portfolios)

# Organize programs
phase_0_programs = [p for p in phase_0_data.get('programs', []) if p.get('portfolio') in FS_PORTFOLIOS]
phase_1_programs = [p for p in phase_1_data.get('programs', []) if p.get('portfolio') in FS_PORTFOLIOS]

# Phase 2 programs
phase_2_programs = []
for p in execution_data.get('programs', []):
    if p.get('portfolio') in FS_PORTFOLIOS:
        p_copy = p.copy()
        p_copy['phase'] = '2'
        p_copy['subcolumn'] = 'inprogress'
        phase_2_programs.append(p_copy)

phase_1_prototyping = [p for p in phase_1_programs if p.get('subcolumn') == 'prototyping']
phase_1_ready = [p for p in phase_1_programs if p.get('subcolumn') == 'ready']
phase_2_ready_bup = [p for p in phase_2_programs if p.get('subcolumn') == 'ready']
phase_2_inprogress = [p for p in phase_2_programs if p.get('subcolumn') == 'inprogress']

teams = teams_data.get('teams', [])
portfolios = FS_PORTFOLIOS

# Calculate stats
def calc_stats(items, health_key):
    stats = {'not_started': 0, 'on_track': 0, 'watch': 0, 'blocked': 0, 'completed': 0}
    for item in items:
        health = (item.get(health_key, 'Unknown') or 'Unknown').lower().replace(' ', '_')
        if 'not_started' in health or health == 'unknown':
            stats['not_started'] += 1
        elif 'on_track' in health:
            stats['on_track'] += 1
        elif 'watch' in health or 'at_risk' in health:
            stats['watch'] += 1
        elif 'blocked' in health or 'off_track' in health:
            stats['blocked'] += 1
        elif 'completed' in health:
            stats['completed'] += 1
        else:
            stats['not_started'] += 1
    return stats

total_programs = len(phase_2_programs)
total_projects = sum(len(p.get('projects', [])) for p in phase_2_programs)
total_epics = sum(len(proj.get('epics', [])) for p in phase_2_programs for proj in p.get('projects', []))

program_stats = calc_stats(phase_2_programs, 'health')
all_projects = [proj for p in phase_2_programs for proj in p.get('projects', [])]
project_stats = calc_stats(all_projects, 'health_status')
all_epics = [epic for proj in all_projects for epic in proj.get('epics', [])]
epic_stats = calc_stats(all_epics, 'health')

# Build programs by capacity
programs_by_capacity = defaultdict(lambda: {'name': '', 'june': 0, 'july': 0, 'august': 0, 'september': 0, 'teams': []})
for team in teams:
    if team.get('june_delivered_by_program'):
        for prog, val in team['june_delivered_by_program'].items():
            programs_by_capacity[prog]['name'] = prog
            programs_by_capacity[prog]['june'] += float(val or 0)
            if team['name'] not in programs_by_capacity[prog]['teams']:
                programs_by_capacity[prog]['teams'].append(team['name'])
    if team.get('july_committed_by_program'):
        for prog, val in team['july_committed_by_program'].items():
            programs_by_capacity[prog]['name'] = prog
            programs_by_capacity[prog]['july'] += float(val or 0)
            if team['name'] not in programs_by_capacity[prog]['teams']:
                programs_by_capacity[prog]['teams'].append(team['name'])

programs_by_capacity_list = sorted(programs_by_capacity.values(), key=lambda x: x['july'], reverse=True)

print(f"Building dashboard with {len(portfolios)} portfolios:", file=sys.stderr)
for p in portfolios:
    print(f"  - {p}", file=sys.stderr)
print(f"Phase 0: {len(phase_0_programs)}, Phase 2: {len(phase_2_programs)}", file=sys.stderr)

# Import the HTML builder module
exec(open('build_dashboard_html.py').read())
