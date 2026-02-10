from rankings import generate_rankings
from datetime import datetime

df = generate_rankings()

# Define inline descriptions for headers
header_descriptions = {
    "Resume Rank": "Wins, losses, strength of schedule",
    "Predictive Rank": "Margins matter more than W/L",
    "Recency Rank": "Last 2 weeks performance",
    "Composite Rank": "Weighted average of all types",
}

# Update column names to include <div class='column-desc'>
new_columns = []
for col in df.columns:
    if col in header_descriptions:
        new_columns.append(
            f"{col}<div class='column-desc'>{header_descriptions[col]}</div>"
        )
    else:
        new_columns.append(col)

df.columns = new_columns

# Generate HTML
table_html = df.to_html(index=False, classes="rankings-table", border=0, escape=False)

updated = datetime.utcnow().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Eric Hoops College Basketball Rankings</title>

<!-- Google Font for header -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&display=swap" rel="stylesheet">

<style>
/* Page background and base text */
body {{
    background-color: #2e3743;  /* dark page background */
    color: #f9fafb;
    font-family: "Segoe UI", Roboto, Helvetica, sans-serif;
    margin: 40px;
}}

/* Dashboard header */
.dashboard-header {{
    max-width: 1100px;
    margin: 0 auto 1rem auto;
}}

.dashboard-header h1 {{
    font-family: "Montserrat", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: 600;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #f9fafb;  /* white-ish header text */
}}

/* Methodology card */
.purpose-card {{
    margin-top: 1rem;
    padding: 1rem 1.25rem;
    background: #ffffff;        /* light card */
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    max-width: 900px;
    border-left: 4px solid #3b82f6;
}}

.purpose-card strong {{
    display: block;
    font-size: 0.9rem;
    color: #1f2937;
    margin-bottom: 0.25rem;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}}

.purpose-card p {{
    margin: 0;
    font-size: 0.95rem;
    color: #374151;
    line-height: 1.5;
}}

/* Subtitle / Updated date */
.subtitle {{
    font-size: 0.85rem;
    color: #f9fafb;
    margin-top: 0.25rem;
    text-align: left;
}}

/* Table wrapper */
.table-wrapper {{
    max-width: 1100px;
    margin: 0 auto;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    background-color: #d1d5db;  /* medium-light gray */
    overflow-x: auto;           /* allow horizontal scroll if table too wide */
    padding: 0;                 /* remove wrapper padding */
}}

/* Table styles */
.rankings-table {{
    border-collapse: collapse;
    width: 100%;                /* table spans wrapper */
    background: #e5e7eb;        /* slightly lighter gray than wrapper */
    color: #1f2937;
    table-layout: auto;          /* auto column sizing */
}}

.rankings-table th,
.rankings-table td {{
    padding: 12px 16px;
    text-align: center;          /* center headers and data */
    border-bottom: 1px solid #cbd5e1;
}}

.rankings-table th {{
    background-color: #d6d8db;   /* slightly darker than table */
    color: #1f2937;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.85em;
}}

.column-desc {{
    font-size: 0.65em;
    color: #6b7280;
    margin-top: 2px;
}}

.rankings-table thead th {{
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: #d6d8db;
}}

.rankings-table tr:nth-child(even) {{
    background-color: #eceff1;   /* subtle alternating rows */
}}

.rankings-table tr:hover {{
    background-color: #d6d8db;
}}

.rankings-table td:first-child {{
    font-weight: bold;
}}

/* Responsive adjustment for small screens */
@media (max-width: 768px) {{
    .rankings-table th,
    .rankings-table td {{
        padding: 8px 10px;
        font-size: 0.85rem;
    }}
}}
</style>

<link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/dataTables.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/dataTables.min.js"></script>

</head>

<body>

<div class="dashboard-header">
    <h1>Eric Hoops College Basketball Rankings</h1>

    <div class="purpose-card">
        <strong>Methodology</strong>
        <p>
            These rankings combine resume-based metrics (what teams have accomplished)
            with predictive metrics (how strong they appear) to strike a balance between
            results and true team quality.
        </p>
    </div>

    <div class="subtitle">Updated {updated}</div>
</div>

<div class="table-wrapper">
    {table_html}
</div>

<script>
$(document).ready(function() {{
    $('.rankings-table').DataTable({{
        paging: false,
        info: false,
        searching: false,
        columnDefs: [{{
            targets: '_all',
            orderSequence: ["asc","desc"]
        }}]
    }} );
}});
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
