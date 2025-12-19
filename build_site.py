from rankings import generate_rankings
from datetime import datetime

df = generate_rankings()


table_html = df.to_html(
    index=False,
    classes="rankings-table",
    border=0
)

updated = datetime.utcnow().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Eric Hoops College Basketball Rankings</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 40px;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 8px;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}

        .rankings-table {{
            border-collapse: collapse;
            margin: auto;
            background: white;
            width: 90%;
            max-width: 1100px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
        }}

        .rankings-table th,
        .rankings-table td {{
            padding: 12px 16px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }}

        .rankings-table th {{
            background-color: #1f3a5f;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
        }}

        .rankings-table thead th {{
    position: sticky;
    top: 0; /* stick to the top of the viewport */
    z-index: 10; /* above everything else */
    background-color: #1f3a5f; /* must set background for sticky */
    color: white;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
  




        .rankings-table tr:nth-child(even) {{
            background-color: #fafafa;
        }}

        .rankings-table tr:hover {{
            background-color: #f0f6ff;
        }}

        .rankings-table td:first-child {{
            font-weight: bold;
        }}
        .legend {{
    max-width: 700px;
    margin: 0 auto 24px;
    background: #fff;
    padding: 10px 14px;  /* slightly smaller padding */
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);  /* lighter shadow */
    font-size: 0.85em;
}}



        .legend ul {{
            margin: 10px 0 0;
            padding-left: 20px;
        }}

        .legend li {{
            margin-bottom: 6px;
        }}

        .legend-note {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 12px;
        }}

    </style>
</head>
<body>
    <h1>Eric Hoops College Basketball Rankings</h1>
    <div class="subtitle">Updated {updated}</div>

    <div class="legend">
    <strong>Ranking Types</strong>
    <ul>
        <li><strong>Resume Rank</strong> — Wins, losses and strength of schedule</li>
        <li><strong>Predictive Rank</strong> — Win and loss margins matter more than W/L </li>
        <li><strong>Recency Rank</strong> — Performance in the last 2 weeks</li>
        <li><strong>Composite Rank</strong> — Weighted average of all ranking types</li>
        </ul>
    </div>
        {table_html}
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
