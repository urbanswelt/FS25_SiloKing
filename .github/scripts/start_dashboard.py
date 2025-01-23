import os
import dash
from dash import dcc, html
import pandas as pd

# Path to the comparison summary file
input_file = "Giants/data/vehicles/comparison_summary.txt"

# Parse summary file into a DataFrame
data = []
with open(input_file, "r") as file:
    current_file = None
    for line in file:
        line = line.strip()
        if line.startswith("Changes detected in:"):
            current_file = line.split(":")[1].strip()
        elif current_file and line:
            data.append({"File": current_file, "Change": line})

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("XML Changes Dashboard", style={"text-align": "center"}),

    dcc.Dropdown(
        id="file-dropdown",
        options=[{"label": file, "value": file} for file in df["File"].unique()],
        placeholder="Select a file",
    ),

    html.Div(id="changes-output")
])

@app.callback(
    dash.dependencies.Output("changes-output", "children"),
    [dash.dependencies.Input("file-dropdown", "value")]
)
def update_output(selected_file):
    if selected_file is None:
        return "Select a file to view changes."
    changes = df[df["File"] == selected_file]["Change"].tolist()
    return html.Ul([html.Li(change) for change in changes])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
