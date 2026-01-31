from rankings import generate_rankings
from datetime import datetime

df = generate_rankings()

# Define inline descriptions for headers
header_descriptions = {
    "Resume Rank": "Wins, losses, strength of schedule",
    "Predictive Rank": "Margins matter more than W/L",
    "Recency Rank": "Last 2 weeks performance",
    "Composite Rank": "Weighted average of all types"
}

# Update column names to include <div class='column-desc'>
new_columns = []
for col in df.columns:
    if col in header_descriptions:
        new_columns.append(f"{col}<div class='column-desc'>{header_descriptions[col]}</div>")
    else:
        new_columns.append(col)

df.columns = new_columns

# Generate HTML
table_html = df.to_html(
    index=False,
    classes="rankings-table",
    border=0,
    escape=False  # important! tells Pandas not to escape HTML
)

updated = datetime.utcnow().strftime("%B %d, %Y")

# Corrected f-string with proper JS braces
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
        margin-bottom: 20px;
    }}

    .table-wrapper {{
        max-width: 1100px;
        margin: auto;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .rankings-table {{
        border-collapse: collapse;
        width: 90%;
        margin: auto;
        background: white;
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
        cursor: pointer;
    }}

    .column-desc {{
        font-size: 0.65em;
        color: #ddd;
        margin-top: 2px;
    }}

    .rankings-table thead {{
        display: table-header-group;
    }}

    .rankings-table thead th {{
        position: sticky;
        top: 0;
        z-index: 1000;
        background-color: #1f3a5f;
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
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/dataTables.dataTables.min.css">
<script src="https://cdn.datatables.net/1.13.8/js/dataTables.min.js"></script>
</head>
<body>
<h1>Eric Hoops College Basketball Rankings</h1>
<div class="subtitle">Updated {updated}</div>

<div class="table-wrapper">
    {table_html}
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {{
    new DataTable('.rankings-table', {{
        paging: false,
        info: false,
        searching: false
    }});
}});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
