#!/usr/bin/env python3
"""
Update Program Focus field to N/A for all Phase 2 programs
"""

import json
import subprocess
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "execution_data.json"

def update_program_focus():
    """Update Program Focus to N/A for all programs"""
    # Load execution data
    with open(DATA_FILE, 'r') as f:
        exec_data = json.load(f)

    programs = exec_data.get('programs', [])

    print(f"Found {len(programs)} programs to update")
    print("Updating Program Focus field to 'N/A'...\n")

    success_count = 0
    error_count = 0

    for i, program in enumerate(programs, 1):
        program_id = program.get('id')
        program_name = program.get('name', 'Unknown')

        if not program_id:
            print(f"⚠️  Skipping {program_name} - no ID")
            error_count += 1
            continue

        print(f"[{i}/{len(programs)}] Updating: {program_name[:60]}...")

        # Use Salesforce CLI to update the record
        update_json = json.dumps({
            "Program_Focus__c": "N/A"
        })

        try:
            result = subprocess.run([
                'sf', 'data', 'update', 'record',
                '--target-org', 'gus',
                '--sobject', 'PPM_Program__c',
                '--record-id', program_id,
                '--values', f"Program_Focus__c='N/A'"
            ], capture_output=True, text=True, timeout=10)

            # Check for success in output (CLI warnings go to stderr but still succeed)
            if result.returncode == 0 and 'Success' in result.stdout:
                print(f"   ✅ Success")
                success_count += 1
            else:
                print(f"   ❌ Failed: {result.stdout} {result.stderr}")
                error_count += 1

        except subprocess.TimeoutExpired:
            print(f"   ❌ Timeout")
            error_count += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1

    print(f"\n{'='*60}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total: {len(programs)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    update_program_focus()
