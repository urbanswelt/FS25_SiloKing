import re
import matplotlib.pyplot as plt
from collections import defaultdict

# Path to the comparison summary file
input_file = "Giants/data/vehicles/comparison_summary.txt"

# Parsing the summary file
file_changes = defaultdict(int)
missing_files = []

with open(input_file, "r") as file:
    current_file = None
    for line in file:
        line = line.strip()
        if line.startswith("Changes detected in:"):
            current_file = line.split(":")[1].strip()
        elif line.startswith("File missing in SK_Pack:"):
            missing_files.append(line.split(":")[1].strip())
        elif current_file and line:  # Count changes for the current file
            file_changes[current_file] += 1

# Visualization
files = list(file_changes.keys())
changes = list(file_changes.values())

# Bar Chart
plt.figure(figsize=(10, 6))
plt.barh(files, changes, color="skyblue")
plt.xlabel("Number of Changes")
plt.ylabel("Files")
plt.title("Number of Changes Per File")
plt.tight_layout()
output_chart = "Giants/data/vehicles/change_summary_chart.png"
plt.savefig(output_chart)
plt.show()

# Print missing files
print("Missing files in SK_Pack:")
for missing in missing_files:
    print(f" - {missing}")
