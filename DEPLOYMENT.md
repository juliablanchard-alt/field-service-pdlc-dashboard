# Service Cloud PDLC Dashboard - Deployment Guide

## 🌐 GitHub Pages Deployment (Current)

### Live URL
Your dashboard will be available at:
```
https://service-cloud.github.io/tpm-service-pdlc/
```

### Setup GitHub Pages

1. Go to your repo: https://git.soma.salesforce.com/service-cloud/tpm-service-pdlc
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Click **Save**

The workflow will automatically:
- Generate static HTML from the Flask app
- Deploy to GitHub Pages
- Update daily at 6 AM PT

### Manual Update
To manually update the dashboard:
```bash
cd PDLC/Experiments/phase-dashboard
python3 generate_static.py
git add docs/
git commit -m "Update dashboard static site"
git push origin master
```

---

## 🚀 Heroku Deployment (Recommended for Production)

### Prerequisites
- Heroku account with access
- Heroku CLI installed: `brew install heroku`

### Deploy
```bash
cd PDLC/Experiments/phase-dashboard
heroku login
heroku create service-cloud-pdlc-dashboard
git push heroku main
heroku open
```

### Features on Heroku
- ✅ Real-time data refresh
- ✅ Live GUS queries
- ✅ Auto-refresh every 5 minutes
- ✅ Full Flask app capabilities

---

## 💻 Local Development

### Run Locally
```bash
cd PDLC/Experiments/phase-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
# Open http://localhost:5000
```

### Update Data
```bash
# Fetch latest Phase 0 data
python3 sync_phase0_data.py < /tmp/phase0_sheet.csv

# Fetch latest Phase 2 execution data
python3 fetch_execution_data.py

# Generate static site
python3 generate_static.py
```

---

## 📋 What's Included

### Pages
- **Main Dashboard** (`/`) - Phase 0, 1, 2 overview
- **Execution Tracker** (`/execution`) - Detailed Phase 2 program tracking with filtering

### Features
- ✅ Phase 0 sync from Google Sheets
- ✅ Phase 1 PBD validation with reports
- ✅ Phase 2 GUS integration with full health comments
- ✅ Portfolio/Status/Month AND filtering
- ✅ Auto-refresh (Heroku only)
- ✅ Responsive design

---

## 🔄 Auto-Update Schedule

### GitHub Actions (Static Site)
- Runs daily at **6 AM PT**
- Regenerates static HTML
- No GUS access (uses cached data)

### Heroku (Live App)
- Refresh button triggers live GUS fetch
- 5-minute auto-refresh cycle
- Full real-time data

---

## 🎯 Next Steps

1. **Enable GitHub Pages** in repo settings
2. **Request Heroku access** for production deployment
3. **Configure GUS credentials** for automated data refresh
4. **Add to bookmarks**: Share the GitHub Pages URL with the team

---

## 📞 Support

Issues or questions? Post in **#adlc_crew** (C0B6EKSLB6V)
