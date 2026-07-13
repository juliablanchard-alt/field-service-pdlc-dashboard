#!/usr/bin/env python3
"""
Sync Phase 0 data using Claude Code MCP access

This script is meant to be run via: claude code run sync_via_claude.py
"""

import json
import csv
import io
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1y5FS7MxqUT019bVRJuPOIH2H5Tc-8q9gH_6vXq4CMgk/edit?gid=1674131463#gid=1674131463"
SHEET_NAME = "266 DE Priorites"

def main():
    print("Fetching sheet data from Google...")

    # Fetch using MCP - this requires being run in Claude Code context
    # For now, we'll use a subprocess approach that should work
    try:
        # This would normally use MCP directly, but we'll create a helper
        print("⚠️  This script requires Claude Code MCP context")
        print("Run with: /sync-phase0 skill in Claude Code")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
