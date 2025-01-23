import os
import xmltodict
from deepdiff import DeepDiff

# Paths
giants_path = "Giants/data/vehicles"
sk_pack_path = "SK_Pack/vehicles"
output_file = os.path.join(giants_path, "comparison_summary.txt")

# Function to read and parse XML files
def read_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return xmltodict.parse(file.read())

# Collecting differences
summary = []

for root, _, files in os.walk(giants_path):
    for file in files:
        if file.endswith(".xml"):
            giants_file = os.path.join(root, file)
            relative_path = os.path.relpath(giants_file, giants_path)
            sk_pack_file = os.path.join(sk_pack_path, relative_path)

            if os.path.exists(sk_pack_file):
                giants_data = read_xml(giants_file)
                sk_pack_data = read_xml(sk_pack_file)

                # Comparing XML data
                diff = DeepDiff(giants_data, sk_pack_data, ignore_order=True)

                if diff:
                    summary.append(f"Changes detected in: {relative_path}")
                    summary.append(str(diff))
                    summary.append("")  # Add a blank line for readability
            else:
                summary.append(f"File missing in SK_Pack: {relative_path}")
                summary.append("")  # Add a blank line for readability

# Generating the output
if not summary:
    output = "XML Comparison Summary\n\nNo changes detected."
else:
    output = "XML Comparison Summary\n\n" + "\n".join(summary)

# Writing to the output file
with open(output_file, "w") as out_file:
    out_file.write(output)
