#!/usr/bin/env python3
"""Rebuild GitHub Pages index.html with scheduled build and PM data"""
import json
import re

# Load data
with open('data/execution_data.json', 'r') as f:
    execution_data = json.load(f)

programs = execution_data.get('programs', [])

# Read current GitHub Pages HTML
with open('docs/index.html', 'r') as f:
    html = f.read()

# For each program in Phase 2 In Progress, extract scheduled builds and add to HTML
def get_scheduled_builds(program):
    """Extract unique scheduled builds from program's epics"""
    builds = set()
    for project in program.get('projects', []):
        for epic in project.get('epics', []):
            build = epic.get('scheduled_build', '').strip()
            if build and build != '-':
                builds.add(build)
    return sorted(builds)

# Find and replace each program card to add scheduled build
for program in programs:
    program_name = program['name']
    portfolio = program['portfolio']
    pm = program.get('program_manager', '')
    scheduled_builds = get_scheduled_builds(program)

    # Pattern: program card with this name
    pattern = rf'(<div class="program-card" data-portfolio="{re.escape(portfolio)}">\s*<div class="program-name"[^>]*>{re.escape(program_name)}</div>\s*<div style="margin-bottom: 12px;">)'

    # Build scheduled build badge HTML
    build_badge = ''
    if scheduled_builds:
        build_str = ', '.join(scheduled_builds)
        build_badge = f'<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 12px; color: #dc2626; font-weight: 600; background: #fef2f2; padding: 4px 10px; border-radius: 6px;">🎯 {build_str}</span>'

    # Build PM meta HTML
    pm_meta = ''
    if pm:
        pm_meta = f'<div class="meta-item"><span class="meta-label">PM:</span> {pm}</div>'

    # Replacement with flex container for badges
    replacement = rf'\1<div style="margin-bottom: 12px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">'

    def replacer(match):
        # Get the portfolio badge from the match
        start_pos = match.end()
        # Find the portfolio span
        portfolio_match = re.search(r'(<span style="display: inline-block;[^>]*>' + re.escape(portfolio) + r'</span>)', html[start_pos:start_pos+300])
        if portfolio_match:
            portfolio_span = portfolio_match.group(1)
            # Build new HTML
            new_html = match.group(1).replace('margin-bottom: 12px;', 'margin-bottom: 12px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap;')
            new_html += portfolio_span
            if build_badge:
                new_html += '\n                                    ' + build_badge
            new_html += '\n                                </div>\n                                <div class="program-meta">'
            if pm_meta:
                new_html += '\n                                    ' + pm_meta
            return new_html
        return match.group(0)

    html = re.sub(pattern, replacer, html, count=1)

# Write back
with open('docs/index.html', 'w') as f:
    f.write(html)

print(f"Updated {len(programs)} programs with scheduled build and PM data")
