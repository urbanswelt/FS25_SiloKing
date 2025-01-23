import os
import xmltodict
from deepdiff import DeepDiff

# Paths
giants_path = "Giants/data/vehicles"
sk_pack_path = "SK_Pack/vehicles"
markdown_file = os.path.join(giants_path, "vehicle.md")

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
                    diff_text = str(diff).replace('\n', '\n    ')
                    summary.append(
                        f"### Changes in {relative_path}\n```text\n{diff_text}\n```\n"
                    )
            else:
                summary.append(f"### File missing in SK_Pack\n- {relative_path}\n")

# Generating the Markdown output
if not summary:
    output = "# XML Comparison Summary\n\nNo changes detected."
else:
    output = "# XML Comparison Summary\n\n" + "\n".join(summary)

# Writing to the Markdown file
with open(markdown_file, "w") as md_file:
    md_file.write(output)
