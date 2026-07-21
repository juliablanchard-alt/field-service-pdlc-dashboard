# Orphaned Epics Dashboard - Data Filtering Summary

## Overview
The Orphaned Epics view shows Field Service epics missing program or project assignments (264+ releases only). These epics require PM/leadership intervention to properly nest in the portfolio hierarchy.

---

## Starting Point
- **2,192 total Field Service epics** in GUS (active, non-completed/cancelled)
- **1,280 initially identified as orphaned** (27,021 PD capacity)

---

## Filters Applied (in order)

### 1. Release Filtering: 264+ Only
**Removes:** Epics scheduled for releases before 264
- Filters out old releases (246, 248, 250, 252, 254, 256, 258, 260, 262)
- Includes mobile releases (FSL.Android, SFS.iOS, etc.) but only 264+
- Allows epics with no release assigned (Backlog, "-")

**Logic:**
- Extract release number from `Scheduled_Build__r.Name`
- For standard releases: match leading digits (264, 266, 264.10)
- For mobile/platform releases: extract ANY 3-digit number (`\b(\d{3})\b`)
  - Examples: "FSL.Android.232" → 232, "SFS 258 patch #7" → 258
- Only keep if release_num >= 264 OR no release assigned

---

### 2. Team Filtering: Active Teams Only
**Removes:** Epics from 33 inactive/historical teams
- **Filtered out:** 559 epics, 5,654 PD

**Teams removed include:**
- Historical quarter-specific teams (FSL Q4 Team, FSL Q3Q4 Team, Field Service 3x90d)
- Defunct project teams (FSL - Kone, FSL - Talpiot, FSL - Back to Work)
- Test/infrastructure teams (SIT: CRM Eng, PSSAT: Field Service)
- Old mobile teams (Mobile Field Service - iOS, Mobile Field Service - Android)
- Consolidated teams (FSL - Asset - Lifecycle, Field Service Shared CX)

**Current active teams:** 28 teams from `teams_data.json`

---

### 3. Date Filtering: Last Modified Before 2025
**Removes:** Stale work from 2023-2024
- **Filtered out:** All epics with `LastModifiedDate < 2025-01-01`

**Rationale:** Work untouched for over a year is likely abandoned

---

### 4. Date Filtering: 6+ Months Inactive (with exception)
**Removes:** Epics not modified since January 20, 2026
- **Exception:** Keeps epics with 264+ in the NAME (even if old)
  - Matches: `\b(264|266|268|270|272)\b` in epic name
- **Filtered out:** ~260 epics

**Rationale:** Work not touched in 6 months is likely dormant, unless explicitly tied to current releases by name

---

### 5. Owner Filtering: Inactive Employees
**Removes:** Epics owned by inactive/departed employees
- **Filtered out:** 45 epics, 1,397 PD
- Checks `Owner.IsActive` field in GUS

**Inactive owners include:**
- Ajay Gupta (4 epics, 109 PD)
- Andy Funston (1 epic, 101 PD)
- Hiromichi Cho (11 epics, 218 PD)
- Siddharth Mathur (4 epics, 292 PD)
- And 12 others

**Rationale:** Epics owned by departed employees need reassignment or closure

---

### 6. Work Status Filtering: All Work Items Closed
**Removes:** Epics where ALL work items are in terminal states
- **Filtered out:** 55 epics, ~1,600 PD
- Terminal states: Closed, Never, Cancelled, Duplicate

**Rationale:** If all work is closed/nevered, the epic is functionally complete but status not updated

---

### 7. Title Filtering: Old Release Numbers in Epic Name
**Removes:** Epics with old release numbers (246-262) in the title
- **Filtered out:** 40 epics, 1,443 PD
- Pattern: `\b(246|248|250|252|254|256|258|260|262)\b`

**Examples removed:**
- "258 studio leftovers"
- "262 - SFS Mobile - C&S - [Trust] Production Support"
- "260 SFS Mobile Assets - Bug fixing..."
- "[262] Unplanned trust and investigations"

**Rationale:** Epic names explicitly referencing old releases indicate stale/leftover work from prior release cycles

---

## Final Result

### Before Filtering
- **1,280 orphaned epics**
- **27,021 PD capacity**

### After All Filters
- **301 orphaned epics**
- **12,262 PD capacity**
- **22 active teams**
- **6 release groups**

### Total Reduction
- **76% fewer epics** (979 filtered out)
- **55% less capacity** (14,759 PD removed)

---

## What Was Removed (Summary)

| Filter | Epics Removed | PD Removed | Notes |
|--------|--------------|------------|-------|
| Pre-264 releases | ~60 | ~1,768 | Old releases (246-262) |
| Inactive teams | 559 | 5,654 | 33 historical teams |
| Pre-2025 work | 0* | 0* | Already filtered by 6-month rule |
| 6+ months old | ~260 | ~4,639 | Not touched since Jan 2026 |
| Inactive owners | 45 | 1,397 | Departed employees |
| All work closed | 55 | ~1,600 | Functionally complete |
| Old # in title | 40 | 1,443 | Has 246-262 in epic name |
| **TOTAL UNIQUE** | **~979** | **~14,759** | Some overlap between filters |

*Pre-2025 work was a subset of 6+ months old filter

---

## Data Quality Note

The remaining 301 orphaned epics are:
- From **active teams** (28 current teams)
- Scheduled for **264+ releases** or explicitly marked Backlog/Future
- **Modified in 2026** (within last 6 months OR has 264+ in name)
- Owned by **active employees**
- Have **active work items** (not all closed)

These represent genuine GUS hygiene issues requiring PM attention to properly nest in the program/project hierarchy.

---

## Generated: July 20, 2026
