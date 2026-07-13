# PDLC Phase Dashboard

**Purpose**: Visual dashboard to track programs across PDLC phases (0, 1, 2, 3)

**Status**: Experimental / Skeleton

---

## Overview

This dashboard provides a Kanban-style view of programs moving through the Product Development Lifecycle:

- **Phase 0**: Ideation & Concept
- **Phase 1**: Discovery & Prototyping  
- **Phase 2**: Design & Architecture
- **Phase 3**: Development & Testing

---

## Features

✅ **Kanban Board Layout** - Programs organized by phase  
✅ **Progress Tracking** - Visual progress bars for each program  
✅ **Key Milestones** - Next milestone displayed per program  
✅ **Auto-refresh** - Dashboard updates every 30 seconds  
✅ **API Endpoints** - REST API for program data  
✅ **Responsive Design** - Works on desktop and mobile  

---

## Quick Start (Local)

### 1. Install Dependencies
```bash
cd PDLC/Experiments/phase-dashboard
pip install -r requirements.txt
```

### 2. Run Locally
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

---

## Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deploy Steps

```bash
# Login to Heroku
heroku login

# Create new Heroku app
heroku create your-pdlc-dashboard

# Deploy
git add .
git commit -m "Add PDLC phase dashboard"
git push heroku master

# Open in browser
heroku open
```

---

## Project Structure

```
phase-dashboard/
├── app.py                 # Flask application
├── templates/
│   └── index.html         # Dashboard UI
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku process file
├── runtime.txt           # Python version
└── README.md             # This file
```

---

## API Endpoints

### Get All Programs
```
GET /api/programs
```

**Response:**
```json
{
  "Phase 0": [...],
  "Phase 1": [...],
  "Phase 2": [...],
  "Phase 3": [...]
}
```

### Get Programs by Phase
```
GET /api/programs/<phase>
```

**Example:**
```bash
curl https://your-app.herokuapp.com/api/programs/1
```

### Health Check
```
GET /health
```

---

## Current Data Source

Currently uses **sample data** hardcoded in `app.py`.

### To Connect Real Data:

Replace the `PROGRAMS_DATA` dictionary with:
- Database queries (PostgreSQL, MongoDB)
- Google Sheets API
- GUS (Salesforce work tracking)
- PBD Validator reports
- Custom JSON/CSV files

**Example integration:**
```python
# Connect to validation reports
def load_programs_from_reports():
    reports_dir = Path("../../PBD Validator/reports")
    # Parse reports and extract phase info
    # Return programs_data dict
```

---

## Customization

### Add More Phases
Edit `PROGRAMS_DATA` structure in `app.py`:
```python
"Phase 4": [...]
```

### Change Colors
Edit CSS in `templates/index.html`:
```css
.phase-4 .phase-header { 
    background: linear-gradient(135deg, #color1, #color2); 
}
```

### Add Filters
- Filter by PM
- Filter by status
- Filter by completion percentage
- Search programs

---

## Sample Data Structure

```python
{
    "name": "Program Name",
    "pm": "PM Name",
    "status": "Current Status",
    "completion": 75,  # 0-100
    "next_milestone": "Milestone - Date"
}
```

---

## Next Steps (TODOs)

- [ ] Connect to real data source (GUS, PBD reports, etc.)
- [ ] Add authentication
- [ ] Add program detail pages
- [ ] Add drag-and-drop to move programs between phases
- [ ] Add filtering and search
- [ ] Add historical tracking (phase transitions over time)
- [ ] Email notifications for milestone reminders
- [ ] Export to PDF/CSV
- [ ] Mobile app version

---

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Hosting**: Heroku
- **Database**: None (currently using in-memory data)

---

## Environment Variables (Heroku)

None required for skeleton version.

For production:
```bash
heroku config:set DATABASE_URL=your-db-url
heroku config:set SECRET_KEY=your-secret-key
```

---

## Troubleshooting

### Port Issues
Heroku assigns the PORT environment variable. The app reads it:
```python
port = int(os.environ.get('PORT', 5000))
```

### Dependencies
If deploy fails, check `requirements.txt` versions:
```bash
pip freeze > requirements.txt
```

### Logs
View Heroku logs:
```bash
heroku logs --tail
```

---

## Screenshots

**Phase 0 (Ideation)**
- AI-Powered Customer Insights (25% complete)
- Multi-Cloud Integration Hub (10% complete)

**Phase 1 (Discovery)**  
- Service Agent Copilot (90% complete)
- Loyalty Insights Dashboard (75% complete)

**Phase 2 (Design)**
- Commerce Personalization Engine (60% complete)
- Industry Compliance Tracker (45% complete)

**Phase 3 (Development)**
- Case Classification AI (80% complete)
- Real-Time Analytics Platform (95% complete)

---

## License

Internal Salesforce tool - Not for external distribution

---

**Created**: May 28, 2026  
**Status**: Experimental  
**Maintainer**: TPM PDLC Team
