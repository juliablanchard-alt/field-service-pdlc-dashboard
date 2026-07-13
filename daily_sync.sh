#!/bin/bash
#
# Daily Phase 0 Dashboard Sync
#
# This script triggers Claude Code to sync Phase 0 data from Google Sheets
# Schedule with cron: 0 9 * * * /path/to/daily_sync.sh
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR/../../.."
LOG_FILE="$SCRIPT_DIR/sync.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Phase 0 data sync..." | tee -a "$LOG_FILE"

# Run Claude Code with the sync-phase0 skill
cd "$REPO_DIR"
echo "/sync-phase0" | claude --quiet 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync complete" | tee -a "$LOG_FILE"
