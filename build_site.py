from rankings import generate_rankings
from datetime import datetime

df = generate_rankings()

styled_df = (
    df
        .style
        .background_gradient(subset=['Score'], cmap='RdYlGn')
        .format({'Score': '{:.3f}'})
)

table_html = styled_df.to_html()


# table_html = df.to_html(
#     index=False,
#     classes="rankings-table",
#     border=0
# )

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
            background-color: #222;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
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
    </style>
</head>
<body>
    <h1>Eric Hoops College Basketball Rankings</h1>
    <div class="subtitle">Updated {updated}</div>

    <div style="overflow-x:auto;">
        {table_html}
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
