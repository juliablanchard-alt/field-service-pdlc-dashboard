#!/usr/bin/env python3
"""
Process ALL Phase 0 rows from the complete Google Sheet data
Handles all stages: PM Backlog, Prototyping, Ready for Review, Engineering Backlog
"""

import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"

# ALL rows from rows 4-104 of the Field Service sheet
# Format: [Portfolio, Theme, Tier, Stage, Initiative, ..., Feature (col I=8), ..., Status (col Q=16), PM Lead (col R=17), etc.]

all_rows = [
    # Rows 4-50 from first API call
    ['Foundations', '', 'Tier 1', 'PM Backlog (Phase 0)', '', '', '', '', 'Frontline Workforce Management - Phase 2', '', 'Post Dreamforce scope of MWM in Slack', '', 'TRUE', 'FALSE', 'FALSE', 'FALSE', 'Phase 2 - Blocked pending completion of Phase 1 planning with Slack team. Target 7/6', 'Tushar Sharma / Clare Provenzano', 'Anand Komarraju / Sindhubala Ulavapalli', 'Scott Andrus', 'Sheila Christian / John Vollmer'],
    ['Foundations', '', 'Tier 1', 'PM Backlog (Phase 0)', '', '', '', '', 'Assets: Service BOM', '', '', '', 'TRUE', 'FALSE', 'FALSE', '', 'Phase 2 - Starting Agentic-PDLC Phase 0 (PM research)', 'Nishant Sharma', 'TBD', 'Scott Andrus', 'TBD'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Observability Uplift', '', '', '', 'Instrument the customer-facing surfaces that are blind today. EPT, latency, error, and sync telemetry across Service Documents, Record Edit, Inventory flow, and Push notifications, plus Splunk logging that closes the SD 2.0 gap. (RMI-00043894, 00043892, 00043895, 00043896, 00043893)'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Quality - AI Automation Uplift', '', '', '', 'Catch defects short tests miss. Full-day soak testing for leaks/resource accumulation, a snapshot/integration-UI framework for complex screens, an OS beta regression suite before GA, and headless end-to-end tests of native code paths. (RMI-00043534, 00043532, 00043876, 00043531)'],
    ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager — Conditional Visibility of Cards', '', 'Conditional Visibility of cards within AGX screens', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager  — Iteration within the Orchestration', '', 'Iteration within the Orchestration to unlock complex work', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager — Auxiliary Actions', '', 'Auxiliary Actions to capture tasks outside of the core process', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'AGX: Agentic Integration', '', 'AGX One-Pager — Background Agents in the Flow of Work', '', 'Background Agents triggered throughout the job to integrate non-deterministic outputs into the work process', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 3', 'PM Backlog (Phase 0)', 'AGX: Agentic Integration', '', 'AGX One-Pager — Conversational & Voice Experience', '', 'Conversational experience within the guardrails of the AGX metadata for handsfree and flexibile completion of work', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 4', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Templates & Examples', '', 'Templates & Examples shipped on core for easy reference and adoption', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 5', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Customer-Facing Skills', '', 'Customer facing Skills for AGX development using Claude/GPT', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 6', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Debugging & Authoring Confidence', '', 'Debugging for simple testing and development of AGX', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    ['Mobile', '', 'Tier 1', 'Prototyping', 'Field Service Headless Setup', '', '', '', 'Headless 360 - End to end steelthread of Field Service Setup', 'L', '', '', '', '', '', '', '', 'Kara Carreri', 'Oleg Bivol', '', 'Kristen Muramoto'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Developer Experience', '', '', '', 'Auto-provision Claude Code for mobile engineers — MCP servers/CLIs plus persistent settings — to kill per-workspace setup friction. (RMI-00043555)'],
    ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Creation of Data Capture Form Skill Via Natural Language', 'XS', '', '', '', '', '', '', '', 'Kara Carreri'],
    ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture Skill - SFS Flow to Data Capture', 'M', '', '', 'TRUE', 'FALSE', 'FALSE', '', '', 'Kara Carreri'],
    ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture Skill - Image to Data Capture', 'M', '', '', '', '', '', '', '', 'Kara Carreri'],
    ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture - PDF to Data Capture', 'M', '', '', '', '', '', '', '', 'Kara Carreri'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Felix', '', '', '', 'Project Felix', 'L', 'Pre-Dreamforce scope '],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Strengthen Offline & Connectivity', '', '', '', 'Harden the offline-first foundation. Extend cache-first policy to Schedule/Related/Custom List and Inventory, add upload-queue validation, improve conflict resolution, modernize priming (retire C++, fix entity allowlist, admin sort policy), and land the Hyperforce/COIN fix (~$35K/yr). (RMI-00043625, 00043945, 00043944, 00043626, 00043963, 00043965, 00043964)'],
    ['Mobile', '', 'Tier 3', 'PM Backlog (Phase 0)', 'Mobile Security', 'Security & Accessibility', '', '', 'Mobile Security Enhancements (Security SDK)', 'M', '', '', '', '', '', '', '', 'Kara Carreri', 'Graham Oldfield'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Workforce Management', '', '', '', 'Phase 1 of WFM to allow for sales cycles at DF (LWC based solution)', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile AI', 'AI/Agentforce', '', '', 'Voice to Form - Language support (e.g. Spanish to Spanish)', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'App Startup & Screen Performance Uplift: Native Adapter + Direct2LDS', '', '', '', 'Retire platform debt, keep the toolchain current. Fast startup via Native Adapters + Direct2LDS, iOS CocoaPods to SPM (read-only Dec 2026), faster CI + modularization, MSDK 14 uplift for Agentforce v15, and JWT flow for the 266 auth mandate. (RMI-00043616, 00043621, 00043620, 00043617)'],
    ['Mobile', '', '', 'Ready for Review', 'Perf Priming & Upload Queue Improvements', 'Upload Queue', '', '', 'Upload Queue: Validation Errors', 'L', '', '', 'TRUE', 'FALSE', 'FALSE'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile AI', 'AI/Agentforce', '', '', 'Voice to Form - Language translation (e.g. Spanish to English)', 'M'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Perf Priming & Upload Queue Improvements', 'Offline', '', '', 'File priming to allow for pictures/pdfs/etc to be stored offline', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Kara Carreri', 'Graham Oldfield'],
    ['Mobile', '', '', 'Engineering Backlog', 'Mobile Experience: Notification Priority', '', '', '', 'Emergency Appointment Dispatch Notification', 'S', '', '', 'FALSE', 'TRUE', 'FALSE', '', '', 'Sharon Adler', 'Prashanth Moorthy', '', 'Kristen Muramoto', 'Emma Heftman'],
    ['Mobile', '', '', 'Prototyping', 'Mobile Experience: Notification Priority', 'N/A', '', '', 'Mobile Custom Notifications Priority Tiers (platform dependency)', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Sharon Adler', 'Prashanth Moorthy', '', 'Kristen Muramoto', 'Emma Heftman'],
    ['Mobile', '', '', 'Prototyping', 'Location Intelligence: Native GIS Adoption Invesments', '', '', '', 'Work Order Related List Data Layer: Dynamic Map Symbology', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Sharon Adler', '', '', 'Kristen Muramoto', 'Emma Heftman'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Data Capture: Adoption Investments', '', '', '', 'Image Preview Enhancement - Selective photo display (Filter photos) [Suzlon]', 'M', '', '', '', '', '', '', '', 'Sharon Adler'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile Experience: Barcode Scanner', '', '', '', 'Improve barcode scanner experience to support multi-scanning', 'M', '', '', '', '', '', '', '', 'Sharon Adler'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Location Intelligence: Last 30 Meters ', '', '', '', '', '', '', '', '', '', '', '', '', 'Sharon Adler'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Agentic Search', '', '', '', '', '', '', '', '', '', '', '', '', 'Sharon Adler'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Workforce Management', '', '', '', 'Phase 2 of WFM - native experience in Field Service or standalone app', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Data Capture', 'N/A', '', '', 'Data capture on desktop (ABB critical need) (row 24)', 'M', '', '', '', '', '', '', '', 'Sharon Adler', 'Graham Oldfield', '', 'Stephen Coyner'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Ordering of list views (ABB critical need) (row 17)', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Trigger offline mode based on work (Suzlon)', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Live Activity on Field Service Mobile', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Field Service Interactive Quick Start demo', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Migration', '', '', '', 'Migrate Service Reports 1.0 to Document Builder 2.0 — 1,227 customers, projected 63% fewer incidents and 100% fewer Sev1/Sev2. (RMI-00043877)'],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'App Size', '', '', '', "Stay clear of Google Play's 200MB limit and reduce update fragility. Move ESRI/ArcGIS to an Android Dynamic Feature Module (140MB to 95MB) and separate the LMR core module so non-core failures don't fail the whole update. (RMI-00043908, 00043624)"],
    ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Accessibility', '', '', '', 'Track a11y bugs to 90% compliance on the 120-day SLA (P0-P2) with shift-left tooling. (RMI-00043622)'],
    ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Workforce Scheduling Console', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed', '', '', '', 'David'],
    ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Schedule Vitrual appointments', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed', '', '', '', 'Ameya'],
    ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Get Candidates launched from a record page', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
    ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Optimization Transparency: Optimization Hub', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
]

print(f"Processing {len(all_rows)} rows from Google Sheet...")
print("This is a partial list - need to add rows 51-104")
print("\nFor complete sync, need to paste ALL row data from both API calls")

