# How to Refresh Phase 0/1 Data (WORKING METHOD)

## The Problem Today
- MCP tool returns all 124 rows
- But when I tried to process via Bash, only first ~50 rows were accessible
- Agent approach was a black box that filtered too aggressively

## Tomorrow's Simple Workflow

Just tell me:
```
Refresh Phase 0/1 data from Google Sheets
```

I will:

1. **Call MCP tool** to fetch sheet data (1 second)
2. **Process DIRECTLY in my response** - not via Bash/Agent (5 seconds)
   - Simple logic: Include if Stage contains "PM Backlog", "Prototyping", or "Ready for Review"
   - Skip only if BOTH Initiative AND Feature are empty
3. **Show you the count** (e.g., "Found 82 Phase 0, 11 Phase 1")
4. **Ask if it looks right**
5. **Save only if you approve**

## Processing Logic (SIMPLE)
```python
for row in sheet_rows:
    stage = row[3]  # Column D
    initiative = row[4]  # Column E  
    feature = row[8]  # Column I
    
    # Include if stage matches
    if 'PM Backlog' in stage:
        phase = '0'
    elif 'Prototyping' in stage or 'Ready for Review' in stage:
        phase = '1'
    else:
        continue  # Skip
    
    # Use Feature if present, else Initiative
    name = feature if feature else initiative
    
    # Skip if both empty
    if not name:
        continue
    
    # Add to programs
    programs.append({...})
```

## Why This Will Work

✅ **No Bash subprocess** - I'll process data directly  
✅ **All 124 rows accessible** - MCP result is in my context  
✅ **Show count first** - You verify before saving  
✅ **Simple logic** - Easy to debug if wrong  
✅ **Takes 30 seconds** - Not 30 minutes

## Current State

- **File**: 79 Phase 0, 8 Phase 1 (July 20 data)
- **Sheet**: ~82 Phase 0 (your manual count)
- **Difference**: 3 items (acceptable for tonight)

Tomorrow we'll get it exactly right.
