# GitHub Actions Setup Guide

This document explains how to set up GitHub Actions for automated daily dashboard refreshes at 6 AM PT.

## Overview

The dashboard uses GitHub Actions to:
- Fetch fresh data from GUS (Phase 2 execution data and teams data)
- Fetch Phase 0 data from Google Sheets (when configured)
- Rebuild the static GitHub Pages site
- Auto-commit and push changes daily

## Required GitHub Secrets

You need to configure the following secrets in your GitHub repository:

### 1. SFDX_AUTH_URL (Required)

This secret contains the Salesforce CLI authentication URL for org62.

**How to get it:**
```bash
# On your local machine where you're already authenticated with org62:
sf org display --target-org org62 --verbose --json | jq -r '.result.sfdxAuthUrl'
```

**How to add it to GitHub:**
1. Go to your GitHub repo: https://github.com/juliablanchard-alt/field-service-pdlc-dashboard
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SFDX_AUTH_URL`
5. Value: Paste the auth URL from the command above
6. Click **Add secret**

### 2. GOOGLE_SHEETS_DATA (Optional)

This secret is for Google Sheets API access to fetch Phase 0 data.

**Status:** Not yet implemented. Phase 0 data currently requires manual sync.

**Future setup:**
- Use Google Sheets API with service account
- Or use MCP Google Workspace integration with OAuth

---

## GitHub Actions Workflow

### File Location
`.github/workflows/update-dashboard.yml`

### Schedule
- **Cron**: `0 14 * * *` (6 AM PT / 14:00 UTC)
- **Manual Trigger**: Available via GitHub Actions UI

### What It Does

1. **Checkout code**
2. **Set up Python 3.9**
3. **Install dependencies** from requirements.txt
4. **Install Salesforce CLI**
5. **Authenticate with Salesforce** using SFDX_AUTH_URL secret
6. **Fetch Phase 0 data** (currently skipped - needs Google Sheets setup)
7. **Fetch Phase 2 execution data** from GUS Report 00OEE000002tswH2AQ
8. **Fetch teams data** from GUS
9. **Rebuild GitHub Pages** using sync_to_github_pages.py
10. **Commit and push** changes with `[skip ci]` to avoid recursive builds

---

## Manual Trigger

You can manually trigger the workflow:

1. Go to https://github.com/juliablanchard-alt/field-service-pdlc-dashboard/actions
2. Click **Update PDLC Dashboard** workflow
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow**

---

## Local Refresh (Flask App)

When running the Flask app locally on `localhost:5002`, you can refresh data:

### Manual Refresh Button
- Click the **🔄 Refresh Data** button in the top-right of the dashboard
- Calls `/api/refresh` endpoint
- Fetches execution data and teams data from GUS

### Auto-Refresh
- Dashboard automatically refreshes every **5 minutes**
- Only works with Flask app (not on GitHub Pages static site)
- Detects `/api/refresh` endpoint availability

### Command Line
```bash
# Fetch all data manually
python3 fetch_execution_data.py  # Phase 2 from GUS
python3 fetch_teams_data.py      # Teams from GUS

# Phase 0 requires Google Sheets access (manual for now)
# Use Claude Code MCP or set up Google Sheets API

# Rebuild GitHub Pages
python3 sync_to_github_pages.py

# Push to GitHub
git add docs/ data/
git commit -m "Manual dashboard update"
git push github main
```

---

## Troubleshooting

### Workflow Fails on Salesforce Authentication
- **Check**: SFDX_AUTH_URL secret is set correctly
- **Fix**: Regenerate the auth URL and update the secret
```bash
sf org display --target-org org62 --verbose --json | jq -r '.result.sfdxAuthUrl'
```

### Workflow Fails on Data Fetch
- **Check**: GUS report ID `00OEE000002tswH2AQ` is still valid
- **Check**: org62 has access to the report
- **Fix**: Verify report access or update the report ID in `fetch_execution_data.py`

### Phase 0 Data Not Updating
- **Current Status**: Phase 0 requires manual sync (Google Sheets integration pending)
- **Workaround**: Manually sync Phase 0 data locally, then commit
```bash
# With Claude Code MCP
claude --session /path/to/field-service-execution-dashboard
# Then use /sync-phase0 command

# Or set up Google Sheets API
```

### Auto-Refresh Not Working on GitHub Pages
- **Expected**: Auto-refresh only works with Flask app (localhost:5002)
- **GitHub Pages**: Uses static site, updates once daily via GitHub Actions
- **Solution**: Use the Flask app for real-time updates, GitHub Pages for shared viewing

---

## Data Sources

| Data Type | Source | Refresh Method |
|-----------|--------|----------------|
| Phase 0 Programs | Google Sheet `1y5FS7MxqUT019bVRJuPOIH2H5Tc-8q9gH_6vXq4CMgk` | Manual (MCP/API pending) |
| Phase 1 Programs | Cached in `data/phase_1_programs.json` | Manual |
| Phase 2 Execution | GUS Report `00OEE000002tswH2AQ` | GitHub Actions + Manual |
| Teams Data | GUS Queries (Team roster) | GitHub Actions + Manual |

---

## Monitoring

### Check GitHub Actions Runs
https://github.com/juliablanchard-alt/field-service-pdlc-dashboard/actions

### Check Last Update Time
- Look at the dashboard header: "Last Updated: MM/DD/YYYY, HH:MM:SS"
- Check commit history: https://github.com/juliablanchard-alt/field-service-pdlc-dashboard/commits/main

### Email Notifications
GitHub will email you if the workflow fails.

---

## Next Steps

1. ✅ Set up SFDX_AUTH_URL secret
2. ✅ Test manual workflow trigger
3. ⏳ Set up Google Sheets API for Phase 0 automation
4. ⏳ Add email notifications on success/failure
5. ⏳ Add Slack notifications (optional)

---

## Support

- **GitHub Actions Issues**: Check workflow logs in Actions tab
- **Data Issues**: Verify GUS report access and API limits
- **Questions**: Contact Julia Blanchard or file an issue

Last Updated: July 15, 2026
