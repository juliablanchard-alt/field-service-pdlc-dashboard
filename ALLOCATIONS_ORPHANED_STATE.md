# Allocations Orphaned Expand Drawer - Current State
**Date**: 2026-07-23  
**Git Tag**: `allocations-orphaned-stable-2026-07-23`

## DO NOT CHANGE - Current Working State

### Data Structure (unmapped_details.json)
```json
{
  "Team Name": [
    {
      "epic_id": "a0EEE000001234",  // or "no-epic"
      "epic_name": "Epic Name",
      "epic_status": "On Track",  // or null
      "story_points": 42,  // TOTAL across all months
      "work_items": [
        {
          "work_item_name": "W-12345678",
          "work_item_id": "a07EE000001234",
          "scheduled_build": "264",
          "sprint_name": "2026.08a-TeamName",
          "story_points": 3,
          "assignee": "John Doe",
          "status": "In Progress",
          "month": "August"  // "June", "July", "August", or "September"
        }
      ],
      "months": ["June", "July"]  // list of months this epic appears in
    }
  ]
}
```

### Status Badge Colors (DO NOT CHANGE)
**Epic Status Colors:**
- On Track: `#10b981` (green)
- Watch: `#f59e0b` (amber)
- Blocked: `#dc2626` (red)
- Completed: `#60a5fa` (light blue)
- On Hold: `#eab308` (yellow)
- Canceled/Cancelled: `#bca2d3` (light purple/lavender)
- Not Started: `#94a3b8` (grey)

**Work Item Status Colors:**
- Closed: `#6b21a8` (dark purple)
- Complete: `#60a5fa` (light blue)
- In Progress: `#10b981` (green)
- QA In Progress: `#8b5cf6` (purple)
- Triaged: `#008080` (darker teal)
- On Hold: `#eab308` (yellow)
- Canceled/Cancelled: `#bca2d3` (light purple/lavender)
- New: `#2563eb` (blue - matches tab font color)

### UI Rendering Logic (templates/field_service_dynamic.html lines 15069-15210)
**JavaScript Function**: `toggleUnmappedBreakdown(sanitizedTeamName, originalTeamName)`

**For Regular Epics (epic_id !== 'no-epic'):**
```javascript
// Calculate points by month from work_items array
const pointsByMonth = {June: 0, July: 0, August: 0, September: 0};
epic.work_items.forEach(wi => {
    pointsByMonth[wi.month] = (pointsByMonth[wi.month] || 0) + wi.story_points;
});

// Display format:
<a href="GUS_LINK">{epic_name}</a> | <status_badge>
```

**For No-Epic Work Items (epic_id === 'no-epic'):**
```javascript
// Display format (two lines):
Line 1: <a href="GUS_LINK">{work_item_name}</a> | <status_badge>
Line 2: (No epic assignment) | Assigned to: {assignee}
```

**Table Columns:**
1. Team / Epic / Work Item (left-aligned, with expand icon)
2. Teams (center, empty for breakdown rows)
3. June - Capacity Delivered (center, grey text `#64748b`)
4. July - Capacity Committed (center, blue text `#2563eb`)
5. August - Capacity Planned (center, blue text `#2563eb`)
6. September - Capacity Planned (center, blue text `#2563eb`)

### Key CSS Classes (DO NOT REMOVE)
- `.breakdown-unmapped-{sanitizedTeamName}` - Class for all breakdown rows under a team
- `#expand-unmapped-{sanitizedTeamName}` - ID for the expand icon (▸/▾)
- Inline styles handle colors, padding, alignment

### Data Query Logic (populate_aug_sept_capacity.py)
**June (DELIVERED - completed work):**
- Query: `WHERE Closed_On__c >= 2026-06-01T00:00:00Z AND Closed_On__c < 2026-07-01T00:00:00Z`
- Field: Use `Closed_On__c` to determine WHEN work was completed

**July (COMMITTED - scheduled work):**
- Query: `WHERE Sprint__r.Start_Date__c >= 2026-07-01 AND Sprint__r.Start_Date__c < 2026-08-01`
- Field: Use `Sprint__r.Start_Date__c` to determine WHEN work is scheduled

**August (COMMITTED - scheduled work):**
- Primary: Work in sprints starting in August
- Secondary: Unsprinted work with builds 264, 264.0-264.4
- Field: `Sprint__r.Start_Date__c` for sprinted, `Epic__r.Scheduled_Build__r.Name` for unsprinted

**September (COMMITTED - scheduled work):**
- Primary: Work in sprints starting in September
- Secondary: Unsprinted work with builds 264.5, 264.6, 266, 266.0, 266.1
- Field: Same logic as August

**Unmapped Filter:**
- Include work where `project_name not in project_to_program` mapping
- This means epic has no project assignment OR project not in execution_data.json

### Teams Data Structure (teams_data.json)
```json
{
  "teams": [
    {
      "name": "Team Name",
      "june_delivered_unmapped": 7.0,  // MUST match sum of June column in unmapped_details
      "july_committed_unmapped": 4.0,  // MUST match sum of July column in unmapped_details
      "august_committed_unmapped": 12.0,
      "september_committed_unmapped": 8.0,
      "june_delivered_by_program": {"Program A": 50.0},
      "july_committed_by_program": {"Program B": 30.0},
      "august_committed_by_program": {"Program C": 40.0},
      "september_committed_by_program": {}
    }
  ]
}
```

**CRITICAL**: The unmapped values MUST equal the sum of points in that month's column when Orphaned is expanded.

### Known Issue Being Fixed
- June/July unmapped_details don't match june_delivered_unmapped / july_committed_unmapped totals
- Solution: Make populate_aug_sept_capacity.py the single source of truth for ALL 4 months
- Remove dependency on map_capacity_to_programs.py for June/July unmapped

### Scripts to Consolidate
1. `populate_aug_sept_capacity.py` - Make this the ONLY script that:
   - Queries June (by Closed_On__c)
   - Queries July (by Sprint start date)
   - Queries August (by Sprint start date + unsprinted builds)
   - Queries September (by Sprint start date + unsprinted builds)
   - Updates `unmapped_details.json` (for UI expand drawer)
   - Updates `june_delivered_unmapped`, `july_committed_unmapped`, `august_committed_unmapped`, `september_committed_unmapped` in teams_data.json

2. Remove/deprecate:
   - `map_capacity_to_programs.py` (if it updates June/July unmapped)
   - Any other scripts that touch these unmapped fields

### Rollback Instructions
If the consolidated script breaks anything:
```bash
git checkout allocations-orphaned-stable-2026-07-23
cd ~/field-service-execution-dashboard
python3 populate_aug_sept_capacity.py
git push github main --force
```

### Testing Checklist After Changes
- [ ] Orphaned rows expand/collapse for all teams
- [ ] Epic status badges show correct colors
- [ ] Work item status badges show correct colors  
- [ ] June column shows delivered work (closed in June)
- [ ] July column shows committed work (scheduled for July)
- [ ] August column shows committed work (scheduled for August)
- [ ] September column shows committed work (scheduled for September)
- [ ] No-epic work items show assignee on second line
- [ ] FSL - Foundation - Corecodiles shows 7 June + 4 July = 11 total when expanded
- [ ] All team unmapped totals match expanded view column sums
