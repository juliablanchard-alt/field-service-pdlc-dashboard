#!/usr/bin/env python3
"""
Convert Heroku snapshot HTML to Flask template with dynamic data
"""

import re
from pathlib import Path

def convert_heroku_to_template():
    """Convert hardcoded Heroku HTML to Flask template"""

    template_file = Path(__file__).parent / "templates" / "heroku_version.html"
    output_file = Path(__file__).parent / "templates" / "field_service_dynamic.html"

    print(f"Reading {template_file}...")
    with open(template_file, 'r', encoding='utf-8') as f:
        html = f.read()

    print("Converting...")

    # Find the Overview section with phase columns
    # Look for the phase structure pattern
    phase_pattern = r'<div class="phase-column">.*?</div>\s*</div>\s*</div>'

    # Find where the hardcoded program cards start (around line 2758)
    # Replace the entire Overview content area with Flask template

    # Strategy: Find the Overview tab content div and replace its inner content
    # with a Flask loop that generates the same structure

    # First, let's find the portfolio filter options and replace them
    portfolio_section_start = html.find('<div class="portfolio-dropdown"')
    portfolio_section_end = html.find('</div>\n            </div>\n\n        </div>', portfolio_section_start) + 50

    if portfolio_section_start > 0:
        print(f"Found portfolio section at {portfolio_section_start}")

        # Create dynamic portfolio filter
        portfolio_template = '''<div class="portfolio-dropdown" id="portfolio-dropdown">
                <div class="portfolio-actions">
                    <div class="portfolio-action-btn" onclick="selectAllPortfolios()">Select All</div>
                    <div class="portfolio-action-btn" onclick="clearPortfolioFilter()">Clear All</div>
                </div>
                {% for portfolio in portfolios %}
                <div class="portfolio-option" onclick="togglePortfolioCheckbox(this, event)">
                    <input type="checkbox" id="portfolio-{{ loop.index }}" value="{{ portfolio }}" onclick="event.stopPropagation()" onchange="updatePortfolioFilter(event)" tabindex="-1">
                    <label for="portfolio-{{ loop.index }}" onclick="event.stopPropagation(); document.getElementById('portfolio-{{ loop.index }}').click();">{{ portfolio }}</label>
                </div>
                {% endfor %}
            </div>

        </div>'''

        html = html[:portfolio_section_start] + portfolio_template + html[portfolio_section_end:]
        print("✓ Replaced portfolio filter with Flask template")

    # Find and replace the Overview tab phase columns content
    # Look for the div with id="overview-view"
    overview_start = html.find('<div id="overview-view"')
    if overview_start > 0:
        # Find the corresponding closing div
        # This is complex, so let's find the next major section marker
        overview_end = html.find('<div id="execution-view"', overview_start)

        if overview_end > 0:
            print(f"Found overview section from {overview_start} to {overview_end}")

            # Create Flask template for Overview with phase columns
            overview_template = '''<div id="overview-view" class="view active">
        <!-- Phase Columns -->
        <div style="display: flex; gap: 16px; margin-top: 20px;">

            <!-- Phase 0: Ideation & Prioritization -->
            <div class="phase-column" style="flex: 1; background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="margin-bottom: 16px;">
                    <h2 style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        0️⃣ Ideation & Prioritization
                    </h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 13px;">({{ phase_0_count }})</p>
                </div>

                <!-- Program cards for Phase 0 -->
                {% for program in programs %}
                {% if program.phase == '0' or 'ideation' in (program.name|lower) %}
                <div class="program-card" data-portfolio="{{ program.portfolio }}">
                    <div class="program-name" style="margin-bottom: 8px;">{{ program.name }}</div>

                    <div style="margin-bottom: 12px;">
                        <span style="display: inline-block; font-size: 13px; color: #475569; font-weight: 600; background: #dbeafe; padding: 4px 10px; border-radius: 6px;">{{ program.portfolio }}</span>
                    </div>

                    <div class="program-meta">
                        <div class="meta-item">
                            <span class="meta-label">PM:</span> {{ program.program_manager or 'TBD' }}
                        </div>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
            </div>

            <!-- Phase 1: Discovery & Prototyping -->
            <div class="phase-column" style="flex: 1; background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="margin-bottom: 16px;">
                    <h2 style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        1️⃣ Discovery & Prototyping
                    </h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 13px;">({{ phase_1_count }})</p>
                </div>

                {% for program in programs %}
                {% if program.phase == '1' or 'discovery' in (program.name|lower) %}
                <div class="program-card" data-portfolio="{{ program.portfolio }}">
                    <div class="program-name" style="margin-bottom: 8px;">{{ program.name }}</div>

                    <div style="margin-bottom: 12px;">
                        <span style="display: inline-block; font-size: 13px; color: #475569; font-weight: 600; background: #dbeafe; padding: 4px 10px; border-radius: 6px;">{{ program.portfolio }}</span>
                    </div>

                    <div class="program-meta">
                        <div class="meta-item">
                            <span class="meta-label">PM:</span> {{ program.program_manager or 'TBD' }}
                        </div>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
            </div>

            <!-- Phase 2: Productization & GTM Initiation -->
            <div class="phase-column" style="flex: 1; background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="margin-bottom: 16px;">
                    <h2 style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        2️⃣ Productization & GTM Initiation
                    </h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 13px;">({{ phase_2_count }})</p>
                </div>

                {% for program in programs %}
                {% if program.phase == '2' or 'productization' in (program.name|lower) %}
                <div class="program-card" data-portfolio="{{ program.portfolio }}">
                    <div class="program-name" style="margin-bottom: 8px;">
                        <a href="https://gus.lightning.force.com/lightning/r/PPM_Program__c/{{ program.id }}/view"
                           target="_blank"
                           rel="noopener noreferrer"
                           style="color: #0176D3; text-decoration: underline; font-size: 15px; font-weight: 600;">
                            {{ program.name }} ↗
                        </a>
                    </div>

                    <div style="margin-bottom: 12px;">
                        <span style="display: inline-block; font-size: 13px; color: #475569; font-weight: 600; background: #dbeafe; padding: 4px 10px; border-radius: 6px;">{{ program.portfolio }}</span>
                    </div>

                    <div class="program-meta">
                        <div class="meta-item">
                            <span class="meta-label">Program Manager:</span> {{ program.program_manager or 'TBD' }}
                        </div>
                    </div>

                    {% if program.target_release %}
                    <div style="margin-top: 16px; padding-top: 16px; border-top: 2px solid #f3f4f6;">
                        <span style="font-size: 13px; font-weight: 500; color: #475569;">
                            🎯 {{ program.target_release }}
                        </span>
                    </div>
                    {% endif %}

                    {% if program.health %}
                    <span class="status-pill pill-{{ program.health|lower|replace(' ', '-') }}" style="position: absolute; top: 16px; right: 16px; font-size: 11px; padding: 4px 8px;">{{ program.health }}</span>
                    {% endif %}
                </div>
                {% endif %}
                {% endfor %}
            </div>

            <!-- Phase 3: GTM Readiness & Adoption -->
            <div class="phase-column" style="flex: 1; background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="margin-bottom: 16px;">
                    <h2 style="color: white; font-size: 18px; font-weight: 600; margin-bottom: 4px;">
                        3️⃣ GTM Readiness & Adoption
                    </h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 13px;">({{ phase_3_count }})</p>
                </div>

                {% set has_phase_3 = namespace(value=False) %}
                {% for program in programs %}
                {% if program.phase == '3' %}
                {% set has_phase_3.value = True %}
                <div class="program-card" data-portfolio="{{ program.portfolio }}">
                    <div class="program-name" style="margin-bottom: 8px;">{{ program.name }}</div>
                </div>
                {% endif %}
                {% endfor %}

                {% if not has_phase_3.value %}
                <div style="text-align: center; padding: 40px; color: rgba(255,255,255,0.6);">
                    <div style="font-size: 48px; margin-bottom: 12px;">🚀</div>
                    <p style="font-size: 16px; font-weight: 500;">No programs launched</p>
                    <p style="font-size: 13px; margin-top: 8px;">Programs ready for GTM will appear here</p>
                </div>
                {% endif %}
            </div>

        </div>
    </div>

    '''

            html = html[:overview_start] + overview_template + html[overview_end:]
            print("✓ Replaced Overview section with Flask template")

    # Save the converted template
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Conversion complete!")
    print(f"Saved to: {output_file}")
    print(f"\nOriginal: {len(html)} characters")
    print(f"Next step: Update app.py to use 'field_service_dynamic.html' template")

if __name__ == "__main__":
    convert_heroku_to_template()
