# PDLC Dashboard Automation Setup

## Current Status: Local Cron Job (Stopgap Solution)

The dashboard automatically updates **twice daily** at 9 AM and 2 PM via a cron job running on Julia's MacBook.

⚠️ **Important Limitations:**
- Requires Julia's Mac to be ON and awake at scheduled times
- Depends on Julia's GUS authentication (org62 access)
- Single point of failure - stops working if Julia is unavailable
- **This is a temporary solution** until Heroku access is granted

---

## How It Works

### Automated Schedule
- **9:00 AM**: Fetch fresh GUS data → rebuild static site → push to GitHub Pages
- **2:00 PM**: Fetch fresh GUS data → rebuild static site → push to GitHub Pages

### What Gets Updated
1. **Phase 2 Execution Data**: From GUS Report `00OEE000002tswH2AQ`
   - Programs, projects, epics
   - Health status, PMs, teams
2. **Teams Roster Data**: From GUS queries
   - Team members, filled/non-filled positions
3. **GitHub Pages Site**: https://julia-blanchard.github.io/field-service-pdlc-dashboard/
   - Rebuilt from latest data
   - Published automatically

### Files Involved
- `auto_update_dashboard.sh` - Main automation script
- `fetch_execution_data.py` - Fetches Phase 2 data from GUS
- `fetch_teams_data.py` - Fetches teams roster from GUS
- `sync_to_github_pages.py` - Rebuilds static GitHub Pages site
- `logs/auto_update.log` - Automation log (check if updates fail)

---

## Checking If It's Working

### View the latest update time
Check the dashboard header at: https://julia-blanchard.github.io/field-service-pdlc-dashboard/

It shows: "Last Updated: MM/DD/YYYY, HH:MM:SS"

### Check the automation log
```bash
tail -50 /Users/julia.blanchard/field-service-execution-dashboard/logs/auto_update.log
```

Look for:
- ✅ "Pushed to GitHub Pages" = Success
- ❌ Error messages = Something failed

### Check recent commits
```bash
cd /Users/julia.blanchard/field-service-execution-dashboard
git log --oneline -5
```

You should see commits like: `Automated dashboard update - 2026-07-15 09:00`

---

## Manual Update (When Needed)

If you need to refresh data outside the scheduled times:

```bash
cd /Users/julia.blanchard/field-service-execution-dashboard
./auto_update_dashboard.sh
```

This runs the same automation immediately.

---

## Cron Job Details

View installed cron jobs:
```bash
crontab -l
```

Current schedule:
```
# PDLC Dashboard auto-update - Runs twice daily (9 AM and 2 PM)
0 9 * * * /Users/julia.blanchard/field-service-execution-dashboard/auto_update_dashboard.sh
0 14 * * * /Users/julia.blanchard/field-service-execution-dashboard/auto_update_dashboard.sh
```

### To disable automation:
```bash
crontab -e
# Comment out or delete the PDLC Dashboard lines
```

### To change schedule:
Edit the cron times (format: `minute hour * * *`)
- `0 9` = 9:00 AM
- `0 14` = 2:00 PM (14:00 in 24-hour time)
- `*/2 9-17` = Every 2 hours from 9 AM to 5 PM

---

## Troubleshooting

### Dashboard not updating?

**1. Check if Mac was awake at scheduled time**
   - Mac must be on and not sleeping for cron to run
   - Check Activity Monitor → Energy to see sleep history

**2. Check the log for errors**
   ```bash
   tail -100 logs/auto_update.log
   ```

**3. Check GUS authentication**
   ```bash
   sf org display --target-org org62
   ```
   If expired, re-authenticate:
   ```bash
   sf org login web --alias org62 --set-default
   ```

**4. Test manually**
   ```bash
   ./auto_update_dashboard.sh
   ```
   If this works but cron doesn't, the issue is with cron setup.

### Git push failed?

Check for merge conflicts:
```bash
git status
git pull github main --rebase
git push github main
```

---

## Long-Term Solution: Heroku

**Why we need Heroku:**
- ☁️ Runs 24/7 in the cloud (not dependent on anyone's laptop)
- 🔐 Independent authentication (not tied to personal GUS access)
- 👥 Team-owned infrastructure
- 🔄 Scheduled refreshes via Heroku Scheduler
- 🌐 Behind Salesforce VPN (proper security)

**Current blocker:**
- Need access to Heroku Enterprise Team with Private Space

**How to get access:**
1. Post in `#heroku-business-operations` Slack channel
2. Request: "I need to deploy Field Service PDLC dashboard to Heroku. Which Enterprise Team/Private Space should I use?"
3. Once access granted, follow deployment steps in `HEROKU_DEPLOYMENT.md` (when created)

---

## When Migrating to Heroku

Once Heroku access is granted:

1. **Disable this cron job**
   ```bash
   crontab -e
   # Remove or comment out PDLC Dashboard lines
   ```

2. **Deploy to Heroku**
   - Follow Service Cloud's setup
   - Use Heroku Scheduler for automated refreshes
   - Keep GitHub Pages as a public snapshot

3. **Update team documentation**
   - Point team to Heroku URL (behind VPN)
   - GitHub Pages becomes secondary/public view

---

## Contact

- **Owner**: Julia Blanchard
- **Questions**: See `#field-service-mobile` Slack channel
- **Heroku Access**: Post in `#heroku-business-operations`

Last Updated: July 15, 2026
