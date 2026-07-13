# 📊 Service Cloud Execution Dashboard - DEMO

## 🎯 What is this?

A **standalone, clickable demo** of the Service Cloud Execution Dashboard. Perfect for:

- **Live demos** in team meetings
- **Email sharing** with stakeholders
- **Async presentations** without needing server access
- **Offline demos** (no internet required!)

## 🚀 How to Use

### Option 1: Open Locally
```bash
# Just double-click the file or run:
open DEMO.html
```

### Option 2: Share via Email/Slack
1. Send the `DEMO.html` file as an attachment
2. Recipient opens it in any browser
3. Fully interactive - no setup needed!

### Option 3: Host on Internal Server
```bash
# Copy to your web server
cp DEMO.html /path/to/your/webserver/
```

## 📸 What's Included

### ✅ Real Data (Snapshot)
- **5 Phase 0 programs** (Planning)
- **2 Phase 1 programs** (Discovery)
- **20 Phase 2 programs** (Productization)

### ✅ All Features Working
- ✨ Beautiful gradient UI
- 📊 Status badges (Blocked, Watch, On Track)
- 📈 Progress bars with completion %
- 🎯 Target release indicators
- 🏷️ "In Dev" badges
- 🎨 Color-coded phases
- ⏰ Timestamp displays

### ✅ Fully Interactive
- Hover effects on cards
- Clickable navigation (visual only)
- Responsive layout
- Professional animations

## 🎨 Demo Mode Features

- **"DEMO MODE" badge** in header (golden animated badge)
- **Curated dataset** showing all status types
- **Fast loading** (single HTML file, ~50KB)
- **No dependencies** (fonts load from Google CDN)

## 📝 Demo Script Suggestions

### For Executives (30 seconds)
> "This is our live execution dashboard tracking 27 programs across 3 phases. Phase 0 shows prototypes under evaluation. Phase 1 is active research. Phase 2 shows 20 programs in development with real-time progress tracking. Notice the color-coded health status and completion bars."

### For Team Members (1 minute)
> "Let me walk through the dashboard. At the top, we see overview metrics. Below, three columns show our phases. Phase 0 programs are being evaluated for prototype review - see the GTM dates and next milestones. Phase 1 shows active discovery work with PM and Arch leads. Phase 2 is our productization phase - see the 'In Dev' badges, health status (Blocked/Watch/On Track), target releases, and progress bars calculated from epic completion."

### For Demos (2 minutes)
> "This dashboard auto-refreshes every 5 minutes. Data comes from GUS for Phase 2 execution tracking and Google Sheets for Phase 0 planning. The progress percentages are calculated live from epic health status. Programs are sorted by priority: blocked first, then watch, then on track. The 'In Dev' badges show active development. Clicking through to the execution tab (in the live version) shows full project and epic breakdowns."

## 🔄 Updating the Demo

To refresh with latest data:

```bash
# From the phase-dashboard directory
cd /Users/eramchand/tpm-service-pdlc/PDLC/Experiments/phase-dashboard

# Generate fresh demo data
python3 << 'EOF'
import json
# ... (copy data generation script from main README)
EOF
```

## 🎯 File Info

- **Size**: ~50KB (lightweight!)
- **Dependencies**: Google Fonts (optional, falls back to system fonts)
- **Browser Support**: All modern browsers (Chrome, Safari, Firefox, Edge)
- **Mobile**: Fully responsive

## 🔐 Security Note

This demo contains **sample data only**. The real dashboard at `http://localhost:5001` has full live data and requires internal access.

---

**Generated**: June 2026  
**Version**: 1.0  
**Contact**: Service Cloud TPM Team
