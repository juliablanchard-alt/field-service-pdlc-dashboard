#!/usr/bin/env python3
"""
Real PBD Validation using the /validate-pbd skill
This script must be run within Claude Code context to access MCP tools
"""

import json
import sys
import subprocess
from pathlib import Path

def validate_pbd_with_skill(pbd_url):
    """
    Run the /validate-pbd skill via Claude Code CLI
    Returns the validation report as a dict
    """
    try:
        # Call Claude Code with the validate-pbd skill
        # This assumes we're in a Claude Code session with MCP access
        result = subprocess.run(
            ['claude', 'code', 'skill', 'validate-pbd', pbd_url],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"Error running validator: {result.stderr}")
            return None

        # Parse the output to extract validation status
        output = result.stdout

        # Extract key information from the validation report
        # This is a simple parser - might need refinement based on actual output
        status = "FAIL"
        completion = 0

        if "✅ PASS" in output and "WARNING" not in output:
            status = "PASS"
        elif "⚠️ PASS WITH WARNINGS" in output:
            status = "PASS WITH WARNINGS"

        # Try to extract completion percentage
        import re
        completion_match = re.search(r'Completion Rate[:\s]+(\d+)%', output)
        if completion_match:
            completion = int(completion_match.group(1))

        return {
            "status": status,
            "completion": completion,
            "report": output
        }

    except Exception as e:
        print(f"Error validating PBD: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_pbd_real.py <pbd_url>")
        sys.exit(1)

    pbd_url = sys.argv[1]
    result = validate_pbd_with_skill(pbd_url)

    if result:
        print(json.dumps(result, indent=2))
    else:
        sys.exit(1)
