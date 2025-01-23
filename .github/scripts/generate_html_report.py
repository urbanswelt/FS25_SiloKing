import os
import pandas as pd

# Paths
summary_file = "Giants/data/vehicles/comparison_summary.txt"
html_report_file = "Giants/data/vehicles/comparison_report.html"

# Read the summary file
with open(summary_file, "r") as file:
    lines = file.readlines()

# Parse the summary into structured data
data = []
current_file = None

for line in lines:
    line = line.strip()
    if line.startswith("Changes detected in:"):
        current_file = line.split(":")[1].strip()
    elif line.startswith("File missing in SK_Pack:"):
        data.append({"File": line.split(":")[1].strip(), "Change": "File missing"})
    elif current_file and line:
        data.append({"File": current_file, "Change": line})

# Convert to a DataFrame
df = pd.DataFrame(data)

# Generate HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>XML Comparison Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ text-align: center; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>XML Comparison Report</h1>
    <table>
        <thead>
            <tr>
                <th>File</th>
                <th>Change</th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in df.iterrows():
    html_content += f"""
        <tr>
            <td>{row['File']}</td>
            <td>{row['Change']}</td>
        </tr>
    """

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Write the HTML report
with open(html_report_file, "w") as html_file:
    html_file.write(html_content)

print(f"HTML report generated: {html_report_file}")
