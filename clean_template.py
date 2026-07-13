#!/usr/bin/env python3
"""
Remove all hardcoded Service Cloud content from template.
Keep:
- Phase 0 (Jinja loop works)
- Execution tab (Jinja loop works)
Replace with empty states:
- Phase 1 (no Field Service data yet)
- Phase 2 (no Field Service data yet)
- Allocations tab (no Field Service data yet)
"""

phase1_empty = '''            <div class="phase-subcolumns">
                <!-- Sub-column 1: Prototyping -->
                <div class="phase-subcolumn prototyping-subcolumn">
                    <div class="subcolumn-header">
                        <span>Prototyping</span>
                        <span class="subcolumn-count">0</span>
                    </div>
                    <div class="empty-state" role="status" aria-live="polite">
                        <div class="empty-state-icon">🔬</div>
                        <div class="empty-state-title">No programs in prototyping</div>
                        <div class="empty-state-text">Programs in discovery will appear here</div>
                    </div>
                </div>

                <!-- Sub-column 2: Ready for Review -->
                <div class="phase-subcolumn ready-subcolumn">
                    <div class="subcolumn-header">
                        <span>Ready for Review</span>
                        <span class="subcolumn-count">0</span>
                    </div>
                    <div class="empty-state" role="status" aria-live="polite">
                        <div class="empty-state-icon">👀</div>
                        <div class="empty-state-title">No programs ready for review</div>
                        <div class="empty-state-text">Programs ready for stakeholder review will appear here</div>
                    </div>
                </div>
            </div>
'''

phase2_empty = '''            <div class="phase-subcolumns">
                <!-- Sub-column 1: Ready for BUP -->
                <div class="phase-subcolumn readybup-subcolumn">
                    <div class="subcolumn-header">
                        <span>Ready for BUP</span>
                        <span class="subcolumn-count">0</span>
                    </div>
                    <div class="empty-state" role="status" aria-live="polite">
                        <div class="empty-state-icon">🎯</div>
                        <div class="empty-state-title">No programs ready for BUP</div>
                        <div class="empty-state-text">Programs ready for business unit planning will appear here</div>
                    </div>
                </div>

                <!-- Sub-column 2: In Progress -->
                <div class="phase-subcolumn inprogress-subcolumn">
                    <div class="subcolumn-header">
                        <span>In Progress</span>
                        <span class="subcolumn-count">0</span>
                    </div>
                    <div class="empty-state" role="status" aria-live="polite">
                        <div class="empty-state-icon">⚙️</div>
                        <div class="empty-state-title">No programs in progress</div>
                        <div class="empty-state-text">Programs in active development will appear here</div>
                    </div>
                </div>
            </div>
'''

allocations_empty = '''    <!-- Allocations Content -->
    <div id="allocations-view" class="view-content">
        <div class="empty-state" role="status" aria-live="polite" style="margin-top: 100px;">
            <div class="empty-state-icon">👥</div>
            <div class="empty-state-title">Team Allocations Not Yet Available</div>
            <div class="empty-state-text">Field Service team allocation data will appear here when available</div>
        </div>
    </div>

    </div><!-- End tab-content -->
</div><!-- End content-wrapper -->

'''

with open('templates/field_service_dynamic.html', 'r') as f:
    lines = f.readlines()

# Find key section boundaries
phase0_start = None
phase1_start = None
phase1_end = None
phase2_start = None
phase2_end = None
phase3_start = None
exec_start = None
alloc_start = None
script_start = None

for i, line in enumerate(lines):
    if 'phase-column phase-0' in line and not phase0_start:
        phase0_start = i
    elif 'phase-column phase-1' in line and not phase1_start:
        phase1_start = i
    elif 'phase-column phase-2' in line and not phase2_start:
        phase2_start = i
        if phase1_start:
            # Phase 1 ends just before Phase 2
            # Find the closing </div> before phase 2
            for j in range(i-1, phase1_start, -1):
                if lines[j].strip() == '</div>':
                    phase1_end = j + 1  # Include the </div>
                    break
    elif 'phase-column phase-3' in line and not phase3_start:
        phase3_start = i
        if phase2_start:
            # Phase 2 ends just before Phase 3
            for j in range(i-1, phase2_start, -1):
                if lines[j].strip() == '</div>':
                    phase2_end = j + 1
                    break
    elif 'id="execution-view"' in line and not exec_start:
        exec_start = i
    elif 'id="allocations-view"' in line and not alloc_start:
        alloc_start = i
    elif alloc_start and '<script>' in line and not script_start:
        script_start = i
        break

print(f"Phase 1: lines {phase1_start} to {phase1_end}")
print(f"Phase 2: lines {phase2_start} to {phase2_end}")
print(f"Allocations: lines {alloc_start} to {script_start}")

# Build new file
new_lines = []

# Keep everything up to Phase 1 subcolumns div
for i in range(phase1_start):
    new_lines.append(lines[i])

# Add Phase 1 header
for i in range(phase1_start, phase1_start + 6):  # Keep header div and title
    new_lines.append(lines[i])

# Add Phase 1 empty state
new_lines.append(phase1_empty + '\n')

# Skip to end of Phase 1, then add closing div
new_lines.append('        </div>\n\n')

# Add Phase 2 header
new_lines.append('        <!-- Phase 2: Productization & GTM Initiation (with 2 sub-columns inside) -->\n')
for i in range(phase2_start, phase2_start + 6):  # Keep header div and title
    new_lines.append(lines[i])

# Add Phase 2 empty state
new_lines.append(phase2_empty + '\n')

# Skip to end of Phase 2, then add closing div
new_lines.append('        </div>\n\n')

# Add Phase 3 through Allocations start (includes all of Execution tab)
for i in range(phase3_start, alloc_start):
    new_lines.append(lines[i])

# Add Allocations empty state
new_lines.append(allocations_empty)

# Add script section to end
for i in range(script_start, len(lines)):
    new_lines.append(lines[i])

# Write new file
with open('templates/field_service_dynamic.html', 'w') as f:
    f.writelines(new_lines)

print(f"\nOriginal: {len(lines)} lines")
print(f"New: {len(new_lines)} lines")
print(f"Removed {len(lines) - len(new_lines)} lines of hardcoded content")
