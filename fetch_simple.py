#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

REPORT_ID = "00OEE0000032xn32AA"
DATA_FILE = Path("data/execution_data.json")

def parse_health(html):
    if not html: return 'Unknown'
    if 'On_Track_Green' in html: return 'On Track'
    if 'Watch_Yellow' in html: return 'Watch'
    if 'Blocked_Red' in html or 'Off_Track_Red' in html: return 'Blocked'
    if 'Not_Started' in html: return 'Not Started'
    return 'Unknown'

print("🔄 Fetching execution data from GUS...")
result = subprocess.run(
    ['sf', 'api', 'request', 'rest', '--target-org', 'gus',
     f'/services/data/v64.0/analytics/reports/{REPORT_ID}',
     '--method', 'GET'],
    capture_output=True, text=True, check=True
)

data = json.loads(result.stdout)
fact_map = data.get('factMap', {})

# Build programs from fact map
programs_map = {}

for key, value in fact_map.items():
    rows = value.get('rows', [])
    for row in rows:
        cells = row.get('dataCells', [])

        # Columns: 0=Target, 1=Health Color, 2=Project, 3=Proj Comments,
        #          4=LOC, 5=Epic Priority, 6=Epic Name, 7=Epic Health Color,
        #          8=Epic Health, 9=Epic Health Comments, 10=Last Modified, 11=Portfolio

        if len(cells) < 3:
            continue

        # Get program name from grouping metadata (extract from reported-upon)
        # For now, extract from context - the grouping info is in extended data
        # We'll need to parse it differently

        target = cells[0].get('label', '')
        project_name = cells[2].get('label', '')
        portfolio = cells[11].get('label', '') if len(cells) > 11 else ''

        # Get program from grouping - need to access via reportExtendedMetadata
        # For now print what we have
        print(f"Target: {target}, Project: {project_name[:30]}, Portfolio: {portfolio}")
        break
    break

print("Data structure needs grouping info - switching approach...")
