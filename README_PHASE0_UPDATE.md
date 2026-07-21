# Phase 0 Google Sheets Update Process

## Current Status (July 20, 2026)
Phase 0 data was last updated: **July 17, 2026** (3 days ago)

## How to Update Phase 0 Data

### Option 1: Ask Claude Code (EASIEST)
Simply say to Claude Code:
```
Update Phase 0 data from the Google Sheet
```

Claude Code will:
1. Fetch the latest data from Google Sheets using MCP
2. Parse the rows
3. Update `/data/phase_0_programs.json`
4. Rebuild the dashboard HTML

### Option 2: Manual Script (for automation)
**Coming Soon**: Automated script that can run in cron/Heroku

The challenge: Google Sheets access requires either:
- Claude Code MCP server (works locally, not in Heroku)
- Google Sheets API with service account (works in Heroku, needs setup)

## Why Phase 0 Isn't Auto-Updating Yet

Unlike GUS data (which uses SF CLI), Google Sheets requires:
1. **Local**: Claude Code with Google Workspace MCP server configured
2. **Heroku**: Google Sheets API credentials + service account setup

## Next Steps for Full Automation

1. Create a Google Cloud service account
2. Grant it access to the Phase 0 Google Sheet
3. Add credentials to Heroku config vars
4. Create Python script using `gspread` library
5. Add to Heroku Scheduler (same schedule as GUS fetches)

**For now**: Ask Claude Code to update Phase 0 data when needed
**Future**: Fully automated like GUS data

## Google Sheet Details
- **Sheet ID**: `1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c`
- **Tab**: `Phase 0 & Phase 1 Priorites`
- **Range**: `A1:Z1000`
- **Output**: `/data/phase_0_programs.json`
