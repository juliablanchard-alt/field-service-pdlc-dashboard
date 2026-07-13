#!/usr/bin/env python3
"""Convert markdown validation reports to HTML"""

import markdown2
from pathlib import Path

REPORTS_DIR = Path(__file__).parent / "validation_reports"
STATIC_DIR = Path(__file__).parent / "static" / "validation_reports"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f5f7fa;
            color: #111827;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #1e40af; margin-bottom: 20px; font-size: 2em; }}
        h2 {{ color: #059669; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }}
        h3 {{ color: #0891b2; margin-top: 20px; margin-bottom: 10px; }}
        strong {{ color: #374151; }}
        ul, ol {{ margin-left: 25px; margin-bottom: 15px; }}
        li {{ margin-bottom: 8px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border: 1px solid #e5e7eb; }}
        th {{ background: #f3f4f6; font-weight: 600; }}
        tr:hover {{ background: #f9fafb; }}
        hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 30px 0; }}
        .status-pass {{ color: #059669; font-weight: 600; }}
        .status-warning {{ color: #d97706; font-weight: 600; }}
        .status-fail {{ color: #dc2626; font-weight: 600; }}
        code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>
"""

for md_file in REPORTS_DIR.glob("*.md"):
    print(f"Converting {md_file.name}...")

    # Read markdown
    md_content = md_file.read_text()

    # Convert to HTML
    html_content = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks"])

    # Apply status colors
    html_content = html_content.replace("✅ PASS", '<span class="status-pass">✅ PASS</span>')
    html_content = html_content.replace("⚠️ PASS WITH WARNINGS", '<span class="status-warning">⚠️ PASS WITH WARNINGS</span>')
    html_content = html_content.replace("❌ FAIL", '<span class="status-fail">❌ FAIL</span>')

    # Wrap in template
    title = md_file.stem.replace("_", " ")
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)

    # Save HTML
    html_file = STATIC_DIR / f"{md_file.stem}.html"
    html_file.write_text(full_html)
    print(f"  → {html_file.name}")

print(f"\n✅ Converted {len(list(REPORTS_DIR.glob('*.md')))} reports to HTML")
