#!/usr/bin/env python3
"""
Auto-discover Field Service Portfolios from GUS
Instead of hardcoding portfolio names, query GUS to find all active
Field Service portfolios dynamically.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "portfolios_discovered.json"
TARGET_ORG = "org62"

def sf_api_request(endpoint):
    """Execute REST API request via sf CLI"""
    try:
        result = subprocess.run(
            ['sf', 'api', 'request', 'rest', '--target-org', TARGET_ORG,
             endpoint, '--method', 'GET'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error executing API request: {e}")
        if hasattr(e, 'stderr'):
            print(f"Stderr: {e.stderr}")
        return None

def sf_data_query(query):
    """Execute SOQL query using sf data query command"""
    try:
        result = subprocess.run(
            ['sf', 'data', 'query', '--target-org', TARGET_ORG,
             '--query', query, '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data.get('result', {}).get('records', [])
    except Exception as e:
        print(f"Error executing query: {e}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        return []

def discover_field_service_portfolios():
    """
    Query GUS to find all active portfolios related to Field Service.
    """
    query = """
    SELECT Id, Name, Status__c, Description__c
    FROM PPM_Portfolio__c
    WHERE (Name LIKE '%Field Service%'
           OR Name LIKE '%264%'
           OR Name LIKE '%266%'
           OR Name LIKE '%268%'
           OR Name LIKE '%SFS%')
    ORDER BY Name
    """

    print("\nQuerying for Field Service portfolios...")
    records = sf_data_query(query)
    print(f"Found {len(records)} Field Service portfolios")

    return records

def discover_programs_for_portfolios(portfolio_ids):
    """
    For each discovered portfolio, find its programs
    """
    if not portfolio_ids:
        return []

    portfolio_id_str = "','".join(portfolio_ids)

    query = f"""
    SELECT Id, Name, Portfolio__r.Name, Portfolio__c, Status__c, Health__c
    FROM PPM_Program__c
    WHERE Portfolio__c IN ('{portfolio_id_str}')
    ORDER BY Portfolio__r.Name, Name
    """

    print(f"\nQuerying programs for {len(portfolio_ids)} portfolios...")
    records = sf_data_query(query)
    print(f"Found {len(records)} programs")

    return records

def main():
    """Main execution flow"""
    print("=" * 60)
    print("Auto-Discovering Field Service Portfolios")
    print("=" * 60)

    # Discover portfolios
    portfolios = discover_field_service_portfolios()

    if not portfolios:
        print("\n❌ No portfolios found")
        return

    # Print discovered portfolios
    print("\n📊 Discovered Portfolios:")
    for p in portfolios:
        print(f"  - {p['Name']} (ID: {p['Id']}, Status: {p.get('Status__c', 'N/A')})")

    # Get portfolio IDs
    portfolio_ids = [p['Id'] for p in portfolios]

    # Discover programs for these portfolios
    programs = discover_programs_for_portfolios(portfolio_ids)

    # Group programs by portfolio
    portfolio_map = {}
    for p in portfolios:
        portfolio_map[p['Id']] = {
            'id': p['Id'],
            'name': p['Name'],
            'status': p.get('Status__c', 'Unknown'),
            'description': p.get('Description__c', ''),
            'programs': []
        }

    for prog in programs:
        portfolio_id = prog.get('Portfolio__c')
        if portfolio_id in portfolio_map:
            portfolio_map[portfolio_id]['programs'].append({
                'id': prog['Id'],
                'name': prog['Name'],
                'status': prog.get('Status__c', 'Unknown'),
                'health': prog.get('Health__c', 'Unknown')
            })

    # Convert to list
    portfolio_list = list(portfolio_map.values())

    # Build output
    output = {
        'last_updated': datetime.now().isoformat(),
        'total_portfolios': len(portfolio_list),
        'total_programs': len(programs),
        'portfolios': portfolio_list
    }

    # Save to file
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved portfolio discovery to {DATA_FILE}")
    print(f"\nSummary:")
    print(f"  Portfolios: {len(portfolio_list)}")
    print(f"  Programs: {len(programs)}")

    # Print program counts per portfolio
    print(f"\nPrograms by Portfolio:")
    for portfolio in portfolio_list:
        print(f"  {portfolio['name']}: {len(portfolio['programs'])} programs")

if __name__ == '__main__':
    main()
