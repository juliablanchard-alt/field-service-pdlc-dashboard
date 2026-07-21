# PDLC Dashboard UI Snapshot - July 21, 2026

## Git Reference
**Tag:** `pdlc-stable-2026-07-21`  
**Rollback command:** `git checkout pdlc-stable-2026-07-21`  
**View files at this point:** `git show pdlc-stable-2026-07-21:path/to/file`

---

## Screenshots Needed

To complete this UI snapshot, capture these views in your browser at **localhost:5002**:

### 1. Execution Tab (Default View)
**File to save:** `screenshots/execution-tab-full.png`
- Shows: Programs/Projects/Epics table, stat cards, filters
- Capture: Full page scroll to show multiple programs

### 2. Execution Tab - Expanded Program
**File to save:** `screenshots/execution-expanded-program.png`  
- Click: Any program row to expand projects
- Shows: Nested project/epic hierarchy

### 3. Phase 0 Tab
**File to save:** `screenshots/phase0-tab.png`
- Shows: PM Backlog programs (79 items)
- Capture: Enough to show table structure and data

### 4. Phase 1 Tab  
**File to save:** `screenshots/phase1-tab.png`
- Shows: Prototyping and Ready for Review (8 items)

### 5. Allocations Tab
**File to save:** `screenshots/allocations-tab.png`
- Shows: Team capacity cards with program breakdowns
- Capture: Multiple teams to show layout pattern

### 6. Orphaned Tab
**File to save:** `screenshots/orphaned-tab.png`
- Shows: 150 epics without programs (filtered to 2026 work)
- Capture: Table with releases and epic details

### 7. Hygiene Features (If Enabled Locally)
**File to save:** `screenshots/hygiene-banner.png`
- Shows: "Needs Attention" banner with count
- Shows: Hygiene badges on epic rows (red/yellow/blue)

---

## Layout Components

### Stat Cards (Top of Execution Tab)
**Structure:**
```html
<div class="stat-cards-container">
  <div class="stat-card">
    <h3>PROGRAMS</h3>
    <div class="stat-number">19</div>
    <div class="stat-breakdown">
      <span class="on-track">15 On Track</span>
      <span class="at-risk">2 At Risk</span>
      <span class="off-track">2 Off Track</span>
    </div>
  </div>
  <!-- Repeat for PROJECTS and EPICS -->
</div>
```

**CSS Classes:**
- `.stat-cards-container` - Flexbox container
- `.stat-card` - Individual card with border/shadow
- `.stat-number` - Large number display
- `.stat-breakdown` - Status counts with color coding

### Execution Table
**Structure:**
```html
<table class="execution-table">
  <thead>
    <tr>
      <th>Program / Project / Epic</th>
      <th>PM</th>
      <th>Status</th>
      <th>Health</th>
      <th>Release</th>
      <th>Team</th>
      <th>Capacity</th>
    </tr>
  </thead>
  <tbody>
    <tr class="program-row" data-program="...">
      <!-- Program columns -->
    </tr>
    <tr class="project-row collapsed" data-project="...">
      <!-- Project columns (hidden initially) -->
    </tr>
    <tr class="epic-row collapsed" data-epic="...">
      <!-- Epic columns (hidden initially) -->
    </tr>
  </tbody>
</table>
```

**CSS Classes:**
- `.execution-table` - Main table styling
- `.program-row` - Bold, larger font, expandable
- `.project-row` - Indented, medium weight
- `.epic-row` - Double-indented, normal weight
- `.collapsed` - Hidden until parent expanded

### Team Capacity Cards
**Structure:**
```html
<div class="team-capacity-card">
  <div class="team-header">
    <h3>Team Name</h3>
    <div class="capacity-summary">120 / 150 PD</div>
  </div>
  <div class="program-breakdown">
    <div class="program-bar" style="width: 40%; background: #color">
      <span>Program A (60 PD)</span>
    </div>
    <div class="program-bar" style="width: 35%; background: #color">
      <span>Program B (52.5 PD)</span>
    </div>
    <!-- More programs -->
  </div>
</div>
```

**CSS Classes:**
- `.team-capacity-card` - Card container with border
- `.team-header` - Team name and total capacity
- `.program-breakdown` - Stacked horizontal bars
- `.program-bar` - Individual program allocation bar

### Hygiene Badges
**Structure:**
```html
<span class="hygiene-badge missing-scheduled-build" 
      title="Missing Scheduled Build">
  📅
</span>
<span class="hygiene-badge missing-priority" 
      title="Missing Priority">
  ⚠️
</span>
<span class="hygiene-badge blocked-no-comments" 
      title="Blocked with No Comments">
  🚫
</span>
```

**CSS Classes:**
- `.hygiene-badge` - Base badge styling (small, rounded)
- `.missing-scheduled-build` - Red background
- `.missing-priority` - Yellow background
- `.missing-owner` - Orange background
- `.blocked-no-comments` - Blue background

### Orphaned Tab Table
**Structure:**
```html
<table class="orphaned-table">
  <thead>
    <tr>
      <th>Epic Name</th>
      <th>Team</th>
      <th>Release</th>
      <th>Capacity</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="epic-name">
        <a href="gus-link">Epic Name</a>
        <div class="hygiene-badges"><!-- badges --></div>
      </td>
      <!-- More columns -->
    </tr>
  </tbody>
</table>
```

**CSS Classes:**
- `.orphaned-table` - Table with left-justified releases
- `.epic-name` - Epic name column with badges
- `.release-cell` - Left-aligned, not centered

---

## Color Scheme

### Status Colors
- **On Track:** `#28a745` (green)
- **At Risk:** `#ffc107` (yellow)  
- **Off Track:** `#dc3545` (red)
- **Blocked:** `#6c757d` (gray)

### Hygiene Badge Colors
- **Missing Scheduled Build:** `#dc3545` (red)
- **Missing Priority:** `#ffc107` (yellow)
- **Missing Owner:** `#fd7e14` (orange)
- **Blocked No Comments:** `#007bff` (blue)

### Portfolio Colors (Program bars)
- **Foundations:** `#17a2b8` (teal)
- **Mobile:** `#6610f2` (purple)
- **Scheduling & Optimization:** `#28a745` (green)
- **Workforce Scheduling:** `#ffc107` (amber)

---

## Key CSS Files

**Main stylesheet:** `static/css/field-service-styles.css`

**Embedded styles in:** `templates/field_service_dynamic.html`
- Lines ~100-500: Base styles
- Lines ~1000-1500: Table layouts
- Lines ~3000-3500: Card components
- Lines ~15000-16000: Hygiene features

---

## JavaScript Interactions

### Expand/Collapse
- Click program row → show/hide projects
- Click project row → show/hide epics
- Toggle icon changes (▶ to ▼)

### Filters
- Month filter → show/hide programs by release
- Portfolio filter → show/hide by portfolio
- Team filter → show/hide by assigned team

### Tab Switching
- Click tab → load corresponding view
- Cache bust parameter prevents stale data

---

## Data Structure

### Execution Data
**File:** `data/execution_data.json`
```json
{
  "programs": [
    {
      "name": "Program Name",
      "program_manager": "PM Name",
      "status": "On Track",
      "health": "Green",
      "target_release": "264",
      "projects": [...]
    }
  ]
}
```

### Phase 0 Data
**File:** `data/phase_0_programs.json`
```json
{
  "last_updated": "2026-07-20T12:27:55",
  "programs": [
    {
      "name": "Feature Name",
      "phase": "0",
      "subcolumn": "backlog",
      "portfolio": "264 Field Service Mobile",
      "stage": "PM Backlog (Phase 0)",
      "program_manager": "PM Name"
    }
  ]
}
```

### Hygiene Data
**File:** `data/hygiene_issues.json`
```json
{
  "epics": [
    {
      "epic_id": "a3QAH...",
      "epic_name": "Epic Name",
      "issues": [
        "missing_scheduled_build",
        "missing_priority"
      ]
    }
  ]
}
```

---

## Rollback Instructions

### To restore this exact UI state:

```bash
cd /Users/julia.blanchard/field-service-execution-dashboard

# Option 1: Create new branch from tag
git checkout -b restore-from-july-21 pdlc-stable-2026-07-21

# Option 2: Reset current branch (DESTRUCTIVE)
git reset --hard pdlc-stable-2026-07-21

# View specific file at this state
git show pdlc-stable-2026-07-21:templates/field_service_dynamic.html

# Compare current vs tagged version
git diff pdlc-stable-2026-07-21 HEAD -- templates/field_service_dynamic.html
```

---

## Next Steps

1. **Capture screenshots:** Open localhost:5002 and save the 7 views above
2. **Commit screenshots:** `git add screenshots/ && git commit -m "UI screenshots for July 21 state"`
3. **Reference this document:** When making UI changes, compare against these screenshots/structure

---

## Related Documentation
- **Memory:** `pdlc_dashboard_state.md` - Current state and to-do list
- **Lessons:** `phase0_refresh_lessons.md` - What went wrong today
- **Instructions:** `REFRESH_PHASE0_TOMORROW.md` - How to refresh Phase 0/1 data correctly
