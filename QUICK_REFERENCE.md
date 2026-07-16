# PDLC Dashboard - Quick Reference

## Current Setup (Stopgap Solution)

**Live Dashboard:** https://julia-blanchard.github.io/field-service-pdlc-dashboard/

**Updates:** Twice daily at 9 AM and 2 PM (your Mac must be on)

**Notifications:** Email to julia.blanchard@salesforce.com

---

## Common Commands

### Check if automation is running
```bash
crontab -l
```

### View recent logs
```bash
tail -50 ~/field-service-execution-dashboard/logs/auto_update.log
```

### Manual update (anytime)
```bash
cd ~/field-service-execution-dashboard
./auto_update_dashboard.sh
```

### Check last update time
Visit dashboard and look at header: "Last Updated: MM/DD/YYYY, HH:MM:SS"

---

## Troubleshooting

### Dashboard didn't update?
1. Check if Mac was awake at 9 AM or 2 PM
2. Check logs: `tail -100 ~/field-service-execution-dashboard/logs/auto_update.log`
3. Check GUS auth: `sf org display --target-org org62`
4. Try manual update: `./auto_update_dashboard.sh`

### No email notification?
- Check spam folder
- Look for subject: "PDLC Dashboard Updated Successfully" or "PDLC Dashboard Update FAILED"
- Check logs to see if email was sent

### GUS authentication expired?
```bash
sf org login web --alias org62 --set-default
```

---

## Pending Items

### Slack Bot Approval (Submitted July 15)
- **Status:** Waiting for admin approval
- **When approved:** Get bot token (starts with `xoxb-...`) and notify Claude Code
- **Will enable:** Slack DM notifications instead of email

### Heroku Enterprise Team Access (Not Yet Requested)
- **Where to ask:** `#heroku-business-operations` Slack channel
- **What to request:** Enterprise Team with Private Space access for Field Service apps
- **Why needed:** Production-grade 24/7 hosting (like Service Cloud has)

---

## Service Cloud vs Current Setup

| Feature | Service Cloud (Heroku) | Current (Local Cron) |
|---------|------------------------|----------------------|
| Hosting | 24/7 cloud | Mac-dependent |
| Refresh | Live Flask app | Static snapshots |
| Auth | Team-owned SFDX URL | Personal GUS login |
| Access | Behind VPN | Public GitHub Pages |
| Owner | Team | Julia |

---

## Files & Locations

**Automation script:** `/Users/julia.blanchard/field-service-execution-dashboard/auto_update_dashboard.sh`

**Logs:** `~/field-service-execution-dashboard/logs/auto_update.log`

**Dashboard repo:** https://github.com/julia-blanchard/field-service-pdlc-dashboard

**Data sources:**
- Phase 2: GUS Report `00OEE000002tswH2AQ`
- Teams: GUS queries
- Phase 0: Google Sheets (manual sync)

**Documentation:**
- Full automation guide: `AUTOMATION_SETUP.md`
- This file: `QUICK_REFERENCE.md`

---

## Contact

**Owner:** Julia Blanchard
**Team:** Field Service Mobile Product Management
**Slack:** `#field-service-mobile`
**Heroku help:** `#heroku-business-operations`

Last Updated: July 15, 2026
