#!/usr/bin/env python3
"""
Complete Phase 0 sync from Field Service Google Sheet
Processes ALL rows and adds Google Sheet row links
"""

import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT_DIR = Path(__file__).parent
JSON_FILE = SCRIPT_DIR / "data" / "phase_0_programs.json"
SPREADSHEET_ID = "1ERWXm6wVS5ItzxCqR6pX1tTf6_ec2_D-jPZeEF5V89c"
GID = "1674131463"  # The gid for "Phase 0 & Phase 1 Priorites" sheet

def get_sheet_url(row_number):
    """Generate a direct link to a specific row in the Google Sheet"""
    return f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={GID}&range=A{row_number}"

def normalize_portfolio(portfolio):
    """Normalize portfolio names to dashboard format"""
    if not portfolio:
        return "TBD"
    if "Field Service" in portfolio:
        return portfolio
    if portfolio == "Foundations":
        return "264 Field Service Foundations"
    elif portfolio == "Mobile":
        return "264 Field Service Mobile"
    elif portfolio == "Workforce Scheduling":
        return "264 Field Service Workforce Scheduling"
    elif portfolio == "Scheduling & Optimization":
        return "264 Field Service Scheduling & Optimization"
    else:
        return f"264 Field Service {portfolio}"

def get_subcolumn(stage):
    """Determine subcolumn based on stage"""
    if "Prototyping" in stage:
        return "prototyping"
    elif "Ready for Review" in stage:
        return "ready_for_review"
    else:
        return "backlog"

def parse_row(row, row_number):
    """Parse a single row into a program object"""
    if len(row) < 9:  # Need at least feature column (I = index 8)
        return None

    portfolio = row[0] if len(row) > 0 else ""
    stage = row[3] if len(row) > 3 else ""
    feature = row[8] if len(row) > 8 else ""
    status = row[16] if len(row) > 16 else ""
    pm_lead = row[17] if len(row) > 17 else ""
    arch_lead = row[18] if len(row) > 18 else ""
    tpm_lead = row[19] if len(row) > 19 else ""
    ux_lead = row[20] if len(row) > 20 else ""
    cx_lead = row[21] if len(row) > 21 else ""

    # Filter for Phase 0 relevant stages
    valid_stages = ["PM Backlog (Phase 0)", "Prototyping", "Ready for Review", "Engineering Backlog"]
    if not feature or not any(s in stage for s in valid_stages):
        return None

    # Skip empty feature names
    if not feature.strip():
        return None

    program = {
        "name": feature,
        "full_name": feature,
        "id": f"sheet_{row_number}",
        "phase": "0",
        "subcolumn": get_subcolumn(stage),
        "portfolio": normalize_portfolio(portfolio),
        "stage": stage,
        "status": status or "",
        "program_manager": pm_lead or "",
        "arch_lead": arch_lead or "",
        "tpm_lead": tpm_lead or "",
        "ux_lead": ux_lead or "",
        "cx_lead": cx_lead or "",
        "health": "Unknown",
        "target_release": "",
        "sheet_url": get_sheet_url(row_number)  # Direct link to the Google Sheet row
    }

    return program

# ALL ROWS FROM THE GOOGLE SHEET (rows 4-104)
# Combined from both API calls
all_sheet_rows = {
    4: ['Foundations', '', 'Tier 1', 'PM Backlog (Phase 0)', '', '', '', '', 'Frontline Workforce Management - Phase 2', '', 'Post Dreamforce scope of MWM in Slack', '', 'TRUE', 'FALSE', 'FALSE', 'FALSE', 'Phase 2 - Blocked pending completion of Phase 1 planning with Slack team. Target 7/6', 'Tushar Sharma / Clare Provenzano', 'Anand Komarraju / Sindhubala Ulavapalli', 'Scott Andrus', 'Sheila Christian / John Vollmer'],
    5: ['Foundations', '', 'Tier 1', 'PM Backlog (Phase 0)', '', '', '', '', 'Assets: Service BOM', '', '', '', 'TRUE', 'FALSE', 'FALSE', '', 'Phase 2 - Starting Agentic-PDLC Phase 0 (PM research)', 'Nishant Sharma', 'TBD', 'Scott Andrus', 'TBD'],
    6: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Observability Uplift', '', '', '', 'Instrument the customer-facing surfaces that are blind today. EPT, latency, error, and sync telemetry across Service Documents, Record Edit, Inventory flow, and Push notifications, plus Splunk logging that closes the SD 2.0 gap. (RMI-00043894, 00043892, 00043895, 00043896, 00043893)'],
    7: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Quality - AI Automation Uplift', '', '', '', 'Catch defects short tests miss. Full-day soak testing for leaks/resource accumulation, a snapshot/integration-UI framework for complex screens, an OS beta regression suite before GA, and headless end-to-end tests of native code paths. (RMI-00043534, 00043532, 00043876, 00043531)'],
    8: ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager — Conditional Visibility of Cards', '', 'Conditional Visibility of cards within AGX screens', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    9: ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager  — Iteration within the Orchestration', '', 'Iteration within the Orchestration to unlock complex work', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    10: ['Mobile', '', 'Tier 1', 'PM Backlog (Phase 0)', 'AGX: Workflow GA Readiness', '', 'AGX One-Pager — Auxiliary Actions', '', 'Auxiliary Actions to capture tasks outside of the core process', '', 'Mature the core functionality of AGX to expand usecases supported and capture more of the Field Service app use cases', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    11: ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'AGX: Agentic Integration', '', 'AGX One-Pager — Background Agents in the Flow of Work', '', 'Background Agents triggered throughout the job to integrate non-deterministic outputs into the work process', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    12: ['Mobile', '', 'Tier 3', 'PM Backlog (Phase 0)', 'AGX: Agentic Integration', '', 'AGX One-Pager — Conversational & Voice Experience', '', 'Conversational experience within the guardrails of the AGX metadata for handsfree and flexibile completion of work', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    13: ['Mobile', '', 'Tier 4', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Templates & Examples', '', 'Templates & Examples shipped on core for easy reference and adoption', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    14: ['Mobile', '', 'Tier 5', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Customer-Facing Skills', '', 'Customer facing Skills for AGX development using Claude/GPT', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    15: ['Mobile', '', 'Tier 6', 'PM Backlog (Phase 0)', 'AGX: Setup Improvement', '', 'AGX One-Pager — Debugging & Authoring Confidence', '', 'Debugging for simple testing and development of AGX', '', 'Deliver meaningful agentic integration embedded into the core job experience delivered by AGX', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Will Carpenter'],
    16: ['Mobile', '', 'Tier 1', 'Prototyping', 'Field Service Headless Setup', '', '', '', 'Headless 360 - End to end steelthread of Field Service Setup', 'L', '', '', '', '', '', '', '', 'Kara Carreri', 'Oleg Bivol', '', 'Kristen Muramoto'],
    17: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Developer Experience', '', '', '', 'Auto-provision Claude Code for mobile engineers — MCP servers/CLIs plus persistent settings — to kill per-workspace setup friction. (RMI-00043555)'],
    18: ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Creation of Data Capture Form Skill Via Natural Language', 'XS', '', '', '', '', '', '', '', 'Kara Carreri'],
    19: ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture Skill - SFS Flow to Data Capture', 'M', '', '', 'TRUE', 'FALSE', 'FALSE', '', '', 'Kara Carreri'],
    20: ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture Skill - Image to Data Capture', 'M', '', '', '', '', '', '', '', 'Kara Carreri'],
    21: ['Mobile', '', 'Tier 2', 'PM Backlog (Phase 0)', 'Data Capture', '', '', '', 'Data Capture - PDF to Data Capture', 'M', '', '', '', '', '', '', '', 'Kara Carreri'],
    22: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Felix', '', '', '', 'Project Felix', 'L', 'Pre-Dreamforce scope '],
    23: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Strengthen Offline & Connectivity', '', '', '', 'Harden the offline-first foundation. Extend cache-first policy to Schedule/Related/Custom List and Inventory, add upload-queue validation, improve conflict resolution, modernize priming (retire C++, fix entity allowlist, admin sort policy), and land the Hyperforce/COIN fix (~$35K/yr). (RMI-00043625, 00043945, 00043944, 00043626, 00043963, 00043965, 00043964)'],
    24: ['Mobile', '', 'Tier 3', 'PM Backlog (Phase 0)', 'Mobile Security', 'Security & Accessibility', '', '', 'Mobile Security Enhancements (Security SDK)', 'M', '', '', '', '', '', '', '', 'Kara Carreri', 'Graham Oldfield'],
    25: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Workforce Management', '', '', '', 'Phase 1 of WFM to allow for sales cycles at DF (LWC based solution)', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    26: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile AI', 'AI/Agentforce', '', '', 'Voice to Form - Language support (e.g. Spanish to Spanish)', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    27: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'App Startup & Screen Performance Uplift: Native Adapter + Direct2LDS', '', '', '', 'Retire platform debt, keep the toolchain current. Fast startup via Native Adapters + Direct2LDS, iOS CocoaPods to SPM (read-only Dec 2026), faster CI + modularization, MSDK 14 uplift for Agentforce v15, and JWT flow for the 266 auth mandate. (RMI-00043616, 00043621, 00043620, 00043617)'],
    28: ['Mobile', '', '', 'Ready for Review', 'Perf Priming & Upload Queue Improvements', 'Upload Queue', '', '', 'Upload Queue: Validation Errors', 'L', '', '', 'TRUE', 'FALSE', 'FALSE'],
    29: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile AI', 'AI/Agentforce', '', '', 'Voice to Form - Language translation (e.g. Spanish to English)', 'M'],
    30: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Perf Priming & Upload Queue Improvements', 'Offline', '', '', 'File priming to allow for pictures/pdfs/etc to be stored offline', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Kara Carreri', 'Graham Oldfield'],
    31: ['Mobile', '', '', 'Engineering Backlog', 'Mobile Experience: Notification Priority', '', '', '', 'Emergency Appointment Dispatch Notification', 'S', '', '', 'FALSE', 'TRUE', 'FALSE', '', '', 'Sharon Adler', 'Prashanth Moorthy', '', 'Kristen Muramoto', 'Emma Heftman'],
    32: ['Mobile', '', '', 'Prototyping', 'Mobile Experience: Notification Priority', 'N/A', '', '', 'Mobile Custom Notifications Priority Tiers (platform dependency)', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Sharon Adler', 'Prashanth Moorthy', '', 'Kristen Muramoto', 'Emma Heftman'],
    33: ['Mobile', '', '', 'Prototyping', 'Location Intelligence: Native GIS Adoption Invesments', '', '', '', 'Work Order Related List Data Layer: Dynamic Map Symbology', 'M', '', '', 'FALSE', 'FALSE', 'FALSE', '', '', 'Sharon Adler', '', '', 'Kristen Muramoto', 'Emma Heftman'],
    34: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Data Capture: Adoption Investments', '', '', '', 'Image Preview Enhancement - Selective photo display (Filter photos) [Suzlon]', 'M', '', '', '', '', '', '', '', 'Sharon Adler'],
    35: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Mobile Experience: Barcode Scanner', '', '', '', 'Improve barcode scanner experience to support multi-scanning', 'M', '', '', '', '', '', '', '', 'Sharon Adler'],
    36: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Location Intelligence: Last 30 Meters ', '', '', '', '', '', '', '', '', '', '', '', '', 'Sharon Adler'],
    37: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Agentic Search', '', '', '', '', '', '', '', '', '', '', '', '', 'Sharon Adler'],
    38: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Workforce Management', '', '', '', 'Phase 2 of WFM - native experience in Field Service or standalone app', 'XS', '', '', 'FALSE', 'FALSE', 'FALSE'],
    39: ['Mobile', '', '', 'PM Backlog (Phase 0)', 'Data Capture', 'N/A', '', '', 'Data capture on desktop (ABB critical need) (row 24)', 'M', '', '', '', '', '', '', '', 'Sharon Adler', 'Graham Oldfield', '', 'Stephen Coyner'],
    40: ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Ordering of list views (ABB critical need) (row 17)', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    41: ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Trigger offline mode based on work (Suzlon)', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    42: ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Live Activity on Field Service Mobile', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    43: ['Mobile', '', '', 'PM Backlog (Phase 0)', '', 'N/A', '', '', 'Field Service Interactive Quick Start demo', 'M', '', '', '', '', '', '', '', 'Nitasha Walia', 'Graham Oldfield', '', 'Stephen Coyner'],
    44: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Migration', '', '', '', 'Migrate Service Reports 1.0 to Document Builder 2.0 — 1,227 customers, projected 63% fewer incidents and 100% fewer Sev1/Sev2. (RMI-00043877)'],
    45: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'App Size', '', '', '', "Stay clear of Google Play's 200MB limit and reduce update fragility. Move ESRI/ArcGIS to an Android Dynamic Feature Module (140MB to 95MB) and separate the LMR core module so non-core failures don't fail the whole update. (RMI-00043908, 00043624)"],
    46: ['Mobile', 'Engineering Priorities', '', 'Engineering Backlog', 'Accessibility', '', '', '', 'Track a11y bugs to 90% compliance on the 120-day SLA (P0-P2) with shift-left tooling. (RMI-00043622)'],
    47: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Workforce Scheduling Console', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed', '', '', '', 'David'],
    48: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Schedule Vitrual appointments', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed', '', '', '', 'Ameya'],
    49: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Get Candidates launched from a record page', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
    50: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Optimization Transparency: Optimization Hub', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
    # Rows 51-104 from second API call
    51: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Crew Management logic + UI', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
    52: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', 'WFS, wfm', '', '', '', 'Complex - Multi-Stage jobs', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed'],
    53: ['Workforce Scheduling', '', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Scheduling Policies - Agentic Experience', '', '', '', 'FALSE', 'FALSE', 'FALSE', '', 'Scope + Priority to be discussed', '', '', '', 'Michal'],
    54: ['Scheduling & Optimization', 'Optimization Platform', '', 'PM Backlog (Phase 0)', 'Optimization analytics [WFS, SFS, Optimization adoption]', 'PRD (Quip)', '', '', 'Optimization  hub redesign for SFS/WFS - Optimization hub metrics', '', '', '', '', '', '', '', '', 'Dori Nahmias'],
    55: ['Scheduling & Optimization', 'Optimization Platform', '', 'PM Backlog (Phase 0)', 'Customer success SFS, WFS', '', '', '', 'Keep scheduled in RSO', '', '', '', '', '', '', '', '', 'Dori Nahmias'],
    56: ['Scheduling & Optimization', 'Optimization Platform', '', 'PM Backlog (Phase 0)', 'Equipement scheduling [WFS, Customer success, Assets]', '', '', '', 'Multi-resource per task (customer success: MDW + Complex work ; equipement)', '', '', '', '', '', '', '', '', 'Dori Nahmias/Itay Sagiv'],
    57: ['Scheduling & Optimization', 'Optimization Platform', '', 'Engineering Backlog', 'Customer success', '', '', '', 'Scheduled jobs: reduce APEX limit consumption (TD)', '', '', '', '', '', '', '', '', 'Dori Nahmias'],
    58: ['Scheduling & Optimization', 'WFM', '', 'Engineering Backlog', 'WFM Shift optimization setup [WFS, WFM FWM, CCaaS]', '', '', '', 'WFM unified shifts policy, rules, objectives (headless + UI)', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    59: ['Scheduling & Optimization', 'Optimization Platform', '', 'PM Backlog (Phase 0)', 'AB Latency', '', '', '', 'AB Latency', '', '', '', '', '', '', '', '', 'Dori Nahmias'],
    60: ['Scheduling & Optimization', 'WFM', '', 'PM Backlog (Phase 0)', 'WFM Shift assignment optimization [WFS, WFM FWM, CCaaS]', '', '', '', 'WFM Shift assignment optimization', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    61: ['Scheduling & Optimization', 'Asset-Centric View', '', 'PM Backlog (Phase 0)', 'Asset Centric View', '', '', '', 'Planner Visualization and exploration (next: insights, actions)', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    62: ['Scheduling & Optimization', 'WFM', '', 'PM Backlog (Phase 0)', 'WFM Worker experience [WFM FWM, CCaaS, WFS]', '', '', '', 'Respect user preferences in optimization', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    63: ['Scheduling & Optimization', 'WFM', '', 'PM Backlog (Phase 0)', 'WFM rules', '', '', '', 'Check rules API', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    64: ['Scheduling & Optimization', 'WFM', '', 'PM Backlog (Phase 0)', 'CCaaS intraday', '', '', '', 'Live intraday optimization for CCaaS', '', '', '', '', '', '', '', '', 'Itay Sagiv'],
    65: ['Scheduling & Optimization', 'WFM', '', 'Engineering Backlog', 'WFM Labor rules', '', '', '', 'Workload balancing', '', '', '', '', '', '', '', '', 'Dori Nahmias/ Itay Sagiv'],
    66: ['Scheduling & Optimization', 'Optimization Platform', 'Tier 3', 'PM Backlog (Phase 0)', '1-Standardized truck route regulations in EU', '', '', '', 'Travel Mode alignment for truck road / routes in Europe (weight regulation under 8.5T)', '', '', '', '', '', '', '', '', 'Amit Mizrahi'],
    67: ['Scheduling & Optimization', 'Optimization Platform', 'Tier 2', 'PM Backlog (Phase 0)', '2-BYO Matrix /Maps data to ES&O engine', '', '', '', "Enrich private/unmapped territories to enable S&O services with customer's matrix/maps", '', '', '', '', '', '', '', '', 'Amit Mizrahi'],
    68: ['Scheduling & Optimization', 'Optimization Platform', 'Tier 1', 'Prototyping', '3-HERE Matrix Routing POC ', '', '', '', 'Evaluation of HERE API services for real-time travel', '', '', '', '', '', '', '', '', 'Amit Mizrahi'],
    69: ['Scheduling & Optimization', 'Optimization Platform', 'Tier 3', 'PM Backlog (Phase 0)', '4-Ferry based routing ', '', '', '', 'Enable filtering of ferry based routing when on-ground alternatives exist', '', '', '', '', '', '', '', '', 'Amit Mizrahi'],
    70: ['Scheduling & Optimization', 'Optimization Platform', '', 'PM Backlog (Phase 0)', 'Features adoption (RVA, etc.)', '', '', '', '', '', '', '', '', '', '', '', ''],
    71: ['Scheduling & Optimization', 'Agentforce', '', 'Engineering Backlog', '1- Scheduling Agent - outbound Engagment', '', '', '', 'Voice outreach (TD platform)', '', '', '', '', '', '', '', '', 'Niv Garber'],
    72: ['Scheduling & Optimization', 'Agentforce', '', 'Engineering Backlog', '2- Scheduling Agent - inbound Engagment', '', '', '', 'Guest Booking using Voice', '', '', '', '', '', '', '', '', 'Niv Garber'],
    73: ['Scheduling & Optimization', 'Agentforce', '', 'Engineering Backlog', '3- Scheduling Agent ', '', '', '', 'Setup add Voice', '', '', '', '', '', '', '', '', 'Niv Garber'],
    74: ['Scheduling & Optimization', 'Agentforce', '', 'Engineering Backlog', '4- Scheduling Agent ', '', '', '', 'Scheduling UX HDX', '', '', '', '', '', '', '', '', 'Niv Garber Sigal Shapira'],
    75: ['Scheduling & Optimization', 'Agentforce', '', 'Engineering Backlog', '5- Unified Scheduling Agent (Workforce Scheduling)', '', '', '', 'Parity\\nEnable a full end-to-end customer-facing experience for the Unified Scheduling Agent all channels Including Voice (Guest & Outbound)', '', '', '', '', '', '', '', '', 'Niv Garber'],
    76: ['', '', '', 'PM Backlog (Phase 0)', '6- Unified Scheduling Agent (Workforce Scheduling)', '', '', '', 'Setup', '', '', '', '', '', '', '', '', 'Niv Garber'],
    77: ['', '', '', 'PM Backlog (Phase 0)', '7- Unified Scheduling Agent (Workforce Scheduling)', '', '', '', 'Supervisor View', '', '', '', '', '', '', '', '', 'Niv Garber'],
    78: ['Scheduling & Optimization', 'Agentforce', '', 'Ready for Review', '8- Dispatcher Agent', '', '', '', 'Fill Gaps with voice outreach \\nImprove Gantt utilization for B2C customers by pulling forward customer-facing appointments using Voice ', '', '', '', '', '', '', '', '', 'Sigal Shapira Niv Garber'],
    79: ['Scheduling & Optimization', 'Agentforce', '', 'Ready for Review', '9- Dispatcher Agent  - Explainability (Optimization)', '', '', '', "Optimization Transparency \\nLets dispatchers ask Agentforce why specific appointments weren't scheduled after an optimization run", '', '', '', '', '', '', '', '', 'Sigal Shapira'],
    80: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '10- Dispatcher Agent - Explainability (Scheduling)', '', '', '', 'Available from anywhere', '', '', '', '', '', '', '', '', 'Sigal Shapira'],
    81: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '11- Dispatcher Agent - Explainability (Resolution)', '', '', '', 'Near-Miss Resolution\\n- Schedule near miss appointments with \\'keep scheduled\\' \\n- Get candidates near miss resolution with sliding & reshuffle\\n- Traceability of automated recommendation vs. manual change\"', '', '', '', '', '', '', '', '', 'Sigal Shapira'],
    82: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '12- Dispatcher Agent - Explainability (Scheduling)', '', '', '', '- Counterfactual Analysis\\n- Near Miss customization point \\n- Agent Prebuilt Recommendations (TD)\\n- Schedule with sliding- which SAs moved and by how much?\\n- Schedule with Reshuffle: Explain why app were unscheduled\"', '', '', '', '', '', '', '', '', 'Sigal Shapira'],
    83: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '13- Scheduling Agent - TTV', '', '', '', 'Headless setup ', '', '', '', '', '', '', '', '', 'Niv Garber'],
    84: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '14- Scheduling Agent - TTV', '', '', '', 'Headless setup AB policies ', '', '', '', '', '', '', '', '', 'Niv Garber'],
    85: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '15- Dispatcher Agent (Adaptive Scheduling)', '', '', '', 'Increase TTV (Headless Setup)', '', '', '', '', '', '', '', '', 'Sigal Shapira'],
    86: ['Scheduling & Optimization', 'Agentforce', '', 'PM Backlog (Phase 0)', '16- Disaptcher Agent (Agentic Dispatcher Experience)', '', '', '', 'AI-native layer that surfaces what matters most daily brief, risks, outliers, executable next actions, designed headless-first to run in the dispatcher console, Slack, mobile, API ( Automation to Resource absence & Fix overlaps)', '', '', '', '', '', '', '', '', 'Sigal Shapira Niv Garber'],
    87: ['Scheduling & Optimization', 'Console', '', 'PM Backlog (Phase 0)', '1 - Gantt & List Capabilities\\n', '', '', '', 'Seerch by lookup fields (PARITY)', '', '', '', '', '', '', '', ''],
    88: ['', 'Console', '', 'PM Backlog (Phase 0)', '2 - Gantt & List Capabilities\\n', '', '', '', 'Quick Absence Creation (PARITY)', '', '', '', '', '', '', '', ''],
    89: ['', '', '', '', '2 - Gantt & List Capabilities', '', '', '', 'Skills Filter Dropdown: Improve the skills selection experience (PARITY)', '', '', '', '', '', '', '', ''],
    90: ['', '', '', '', '2 - Gantt & List Capabilities', '', '', '', 'Push updates for shifts and crews (NEW CAPABILITY)', '', '', '', '', '', '', '', ''],
    91: ['', 'Console', '', 'PM Backlog (Phase 0)', '3 - Gantt & List Capabilities\\n', '', '', '', 'AI Driven / Co-Worker search for gantt and list (INNOVATION✨)', '', '', '', '', '', '', '', ''],
    92: ['', 'Console', '', 'PM Backlog (Phase 0)', '4 - Gantt View for Operations Manager', '', '', '', 'Utilization view (PARITY - 1000 orgs in DC1) ', '', '', '', '', '', '', '', ''],
    93: ['', 'Console', '', 'PM Backlog (Phase 0)', '5 - Gantt & List Capabilities\\n', '', '', '', 'Compact/Comfy views (PARITY)', '', '', '', '', '', '', '', ''],
    94: ['', 'Console', '', 'PM Backlog (Phase 0)', '6 - Gantt & List Capabilities\\n', '', '', '', 'Read Only Gantt (PARITY)', '', '', '', '', '', '', '', ''],
    95: ['', 'Console', '', 'PM Backlog (Phase 0)', '7 - Gantt & List Capabilities\\n', '', '', '', 'Expand the Activity Tracker to support additional actions and persistence (PARITY)', '', '', '', '', '', '', '', ''],
    96: ['', 'Console', '', 'PM Backlog (Phase 0)', '8 - Gantt & List Capabilities\\n', '', '', '', 'Support actions for more 200 records (PARITY)', '', '', '', '', '', '', '', ''],
    97: ['', 'Console', '', 'PM Backlog (Phase 0)', '9 - Gantt & List Capabilities\\n', '', '', '', 'Bookmark Appointments (PARITY - 350 orgs DC1) ', '', '', '', '', '', '', '', ''],
    98: ['Scheduling & Optimization', 'Console', '', 'PM Backlog (Phase 0)', '10 - Advanced Use Cases', '', '', '', 'Crew Management within the Dispatch Experience (NEW CAPABILITY – $12M ACV VOC Opportunity)', '', '', '', '', '', '', '', ''],
    99: ['Scheduling & Optimization', 'Console', '', 'PM Backlog (Phase 0)', '11 - Inteligent Scheduling', '', '', '', 'Gov Cloud: Support "Why" Explainability for Find Candidates (Non-Gemini Model) (NEW CAPABILITY for Gov Cloud) ', '', '', '', '', '', '', '', ''],
    100: ['Scheduling & Optimization', 'Console', '', 'PM Backlog (Phase 0)', '', '', '', '', 'Absence create/edit for Multiple Records ', '', '', '', '', '', '', '', ''],
}

def main():
    print(f"🔄 Processing {len(all_sheet_rows)} rows from Field Service Google Sheet...")

    programs = []
    for row_num, row_data in all_sheet_rows.items():
        program = parse_row(row_data, row_num)
        if program:
            programs.append(program)

    # Save to JSON
    pt_time = datetime.now(ZoneInfo("America/Los_Angeles"))
    data = {
        "last_updated": pt_time.isoformat(),
        "programs": programs
    }

    JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved {len(programs)} Phase 0 programs to {JSON_FILE}")
    print()

    # Group by portfolio and subcolumn
    by_portfolio = {}
    by_subcolumn = {}
    for p in programs:
        portfolio = p.get("portfolio", "TBD")
        subcolumn = p.get("subcolumn", "backlog")
        by_portfolio[portfolio] = by_portfolio.get(portfolio, 0) + 1
        by_subcolumn[subcolumn] = by_subcolumn.get(subcolumn, 0) + 1

    print("Programs by portfolio:")
    for portfolio in sorted(by_portfolio.keys()):
        print(f"   {portfolio}: {by_portfolio[portfolio]}")

    print("\nPrograms by subcolumn:")
    for subcolumn in sorted(by_subcolumn.keys()):
        print(f"   {subcolumn}: {by_subcolumn[subcolumn]}")

    print(f"\n🔗 Each program includes a 'sheet_url' field linking back to the Google Sheet row")
    print(f"   Example: {programs[0]['sheet_url']}")

if __name__ == "__main__":
    main()
