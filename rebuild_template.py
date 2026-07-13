#!/usr/bin/env python3
"""
Rebuild field_service_dynamic.html template by removing bloated execution-view section
and replacing it with proper execution dashboard content
"""

# Read the backup file
with open('templates/field_service_dynamic.html.backup', 'r') as f:
    content = f.read()

# Find the execution-view section
start_marker = '<div id="execution-view" class="view-content">'
start_idx = content.find(start_marker)

# Find the next section (allocations-view)
end_marker = '<div id="allocations-view"'
end_idx = content.find(end_marker, start_idx)

print(f"Found execution-view at index {start_idx}")
print(f"Found allocations-view at index {end_idx}")

# Extract before and after
before = content[:start_idx]
after = content[end_idx:]

# Create new execution view content
execution_view = '''<div id="execution-view" class="view-content">
        <!-- Execution Dashboard: Programs → Projects → Epics Breakdown -->

        <!-- Stats Cards -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
            <!-- Programs Card -->
            <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase;">Programs</span>
                    <span style="font-size: 28px; font-weight: 700; color: #1e293b;">{{ total_execution_programs }}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></div>
                        <span style="color: #64748b; flex: 1;">On Track</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (health_counts.on_track / total_execution_programs * 100) if total_execution_programs > 0 else 0 }}%; height: 100%; background: #10b981;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ health_counts.on_track }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #94a3b8;"></div>
                        <span style="color: #64748b; flex: 1;">Not Started</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (health_counts.not_started / total_execution_programs * 100) if total_execution_programs > 0 else 0 }}%; height: 100%; background: #94a3b8;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ health_counts.not_started }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></div>
                        <span style="color: #64748b; flex: 1;">Watch</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (health_counts.watch / total_execution_programs * 100) if total_execution_programs > 0 else 0 }}%; height: 100%; background: #f59e0b;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ health_counts.watch }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div>
                        <span style="color: #64748b; flex: 1;">Blocked</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (health_counts.blocked / total_execution_programs * 100) if total_execution_programs > 0 else 0 }}%; height: 100%; background: #ef4444;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ health_counts.blocked }}</span>
                    </div>
                </div>
            </div>

            <!-- Projects Card -->
            <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase;">Projects</span>
                    <span style="font-size: 28px; font-weight: 700; color: #1e293b;">{{ total_projects }}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></div>
                        <span style="color: #64748b; flex: 1;">On Track</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (project_stats.on_track / total_projects * 100) if total_projects > 0 else 0 }}%; height: 100%; background: #10b981;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ project_stats.on_track }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #94a3b8;"></div>
                        <span style="color: #64748b; flex: 1;">Not Started</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (project_stats.not_started / total_projects * 100) if total_projects > 0 else 0 }}%; height: 100%; background: #94a3b8;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ project_stats.not_started }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></div>
                        <span style="color: #64748b; flex: 1;">Watch</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (project_stats.watch / total_projects * 100) if total_projects > 0 else 0 }}%; height: 100%; background: #f59e0b;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ project_stats.watch }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div>
                        <span style="color: #64748b; flex: 1;">Blocked</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (project_stats.blocked / total_projects * 100) if total_projects > 0 else 0 }}%; height: 100%; background: #ef4444;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ project_stats.blocked }}</span>
                    </div>
                </div>
            </div>

            <!-- Epics Card -->
            <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase;">Epics</span>
                    <span style="font-size: 28px; font-weight: 700; color: #1e293b;">{{ total_epics }}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></div>
                        <span style="color: #64748b; flex: 1;">On Track</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (epic_stats.on_track / total_epics * 100) if total_epics > 0 else 0 }}%; height: 100%; background: #10b981;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ epic_stats.on_track }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #94a3b8;"></div>
                        <span style="color: #64748b; flex: 1;">Not Started</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (epic_stats.not_started / total_epics * 100) if total_epics > 0 else 0 }}%; height: 100%; background: #94a3b8;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ epic_stats.not_started }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></div>
                        <span style="color: #64748b; flex: 1;">Watch</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (epic_stats.watch / total_epics * 100) if total_epics > 0 else 0 }}%; height: 100%; background: #f59e0b;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ epic_stats.watch }}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 12px;">
                        <div style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></div>
                        <span style="color: #64748b; flex: 1;">Blocked</span>
                        <div style="flex: 2; height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden;">
                            <div style="width: {{ (epic_stats.blocked / total_epics * 100) if total_epics > 0 else 0 }}%; height: 100%; background: #ef4444;"></div>
                        </div>
                        <span style="color: #1e293b; font-weight: 600;">{{ epic_stats.blocked }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Programs Table -->
        <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 16px;">Programs & Projects</div>

            {% for program in execution_programs %}
            <div style="border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 12px; overflow: hidden;">
                <!-- Program Header -->
                <div style="background: #f8fafc; padding: 16px; border-bottom: 1px solid #e2e8f0; cursor: pointer;" onclick="toggleExecutionProgram(this)">
                    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 16px; align-items: center;">
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #1e293b;">{{ program.name }}</div>
                            <div style="font-size: 11px; color: #64748b; margin-top: 4px;">{{ program.portfolio }}</div>
                        </div>
                        <div style="font-size: 12px; color: #64748b;">
                            <span style="font-weight: 500; color: #1e293b;">{{ program.program_manager }}</span>
                        </div>
                        <div>
                            {% if program.health and program.health != 'Unknown' %}
                            <span style="display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 500;
                                {% if 'on track' in program.health.lower() %}background: #d1fae5; color: #065f46;
                                {% elif 'watch' in program.health.lower() %}background: #fed7aa; color: #92400e;
                                {% elif 'blocked' in program.health.lower() %}background: #fecaca; color: #991b1b;
                                {% else %}background: #e2e8f0; color: #475569;{% endif %}">
                                {{ program.health }}
                            </span>
                            {% endif %}
                        </div>
                        <div style="text-align: right; font-size: 12px; color: #64748b;">
                            {{ program.projects|length }} projects
                            <span style="margin-left: 8px;">▼</span>
                        </div>
                    </div>
                </div>

                <!-- Projects (initially hidden) -->
                <div class="program-projects" style="display: none;">
                    {% for project in program.projects %}
                    <div style="padding: 12px 16px; border-bottom: 1px solid #f1f5f9;">
                        <div style="font-size: 12px; font-weight: 500; color: #475569; margin-bottom: 8px;">
                            {{ project.name[:100] }}{% if project.name|length > 100 %}...{% endif %}
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            {% for epic in project.epics %}
                            <div style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 10px; background: #f8fafc; border-radius: 6px; font-size: 11px;">
                                <div style="width: 6px; height: 6px; border-radius: 50%;
                                    {% if 'on track' in epic.health.lower() %}background: #10b981;
                                    {% elif 'watch' in epic.health.lower() %}background: #f59e0b;
                                    {% elif 'blocked' in epic.health.lower() %}background: #ef4444;
                                    {% else %}background: #94a3b8;{% endif %}"></div>
                                <span style="color: #64748b;">{{ epic.name }}</span>
                                <span style="color: #94a3b8;">•</span>
                                <span style="color: #1e293b; font-weight: 500;">{{ epic.health_status }}</span>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    '''

# Combine
new_content = before + execution_view + after

# Write to new file
with open('templates/field_service_dynamic.html', 'w') as f:
    f.write(new_content)

print(f"✅ Template rebuilt!")
print(f"   Before: {len(content):,} bytes")
print(f"   After: {len(new_content):,} bytes")
print(f"   Saved: {len(content) - len(new_content):,} bytes")
