#!/bin/bash
#
# Phase 0 Dashboard Data Sync
# Run this script or schedule it with cron to sync data daily
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/sync.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Phase 0 data sync..." | tee -a "$LOG_FILE"

# Run via Claude Code (which has MCP access)
cd "$SCRIPT_DIR"
claude code run --quiet "$SCRIPT_DIR/sync_via_claude.py" 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync complete" | tee -a "$LOG_FILE"
