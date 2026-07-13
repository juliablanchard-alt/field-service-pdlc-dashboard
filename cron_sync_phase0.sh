#!/bin/bash
# Daily Phase 0 Sync - Runs at 6 AM PT
# This script is designed to be run by cron
# It uses the Claude Code MCP Google integration

cd "$(dirname "$0")"

LOG_FILE="logs/phase0_sync_$(date +%Y%m%d).log"
mkdir -p logs

echo "=================================================="  | tee -a "$LOG_FILE"
echo "Phase 0 Daily Sync - $(date)"  | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

# For now, this is a placeholder that shows how to set up the cron
# The actual sync needs to be triggered through Claude Code with MCP access
# or we need to set up API keys

echo "⚠️  Phase 0 sync requires Claude Code MCP access" | tee -a "$LOG_FILE"
echo "   Manual sync: Use '/sync-phase0' in Claude Code" | tee -a "$LOG_FILE"
echo "   Or run: python3 fetch_phase0_data.py with MCP data" | tee -a "$LOG_FILE"

# Alternative: You can set up with Google Sheets API credentials
# SHEET_ID="1y5FS7MxqUT019bVRJuPOIH2H5Tc-8q9gH_6vXq4CMgk"
# SHEET_NAME="P0 Priorites"
# Then use gsheet API to fetch and pipe to fetch_phase0_data.py

echo "=================================================="  | tee -a "$LOG_FILE"
