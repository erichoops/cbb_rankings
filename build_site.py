from rankings import generate_rankings

df = generate_rankings()

table_html = df.to_html(
    index=False,
    classes="rankings-table",
    border=0
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Eric Hoops College Basketball Rankings</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        th {{
            background-color: #f4f4f4;
            text-align: left;
        }}
    </style>
</head>
<body>
    <h1>Eric Hoops College Basketball Rankings</h1>
    {table_html}
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
