import xmltodict

XML_FILE = "modDesc.xml"
README_FILE = "README.md"

def extract_data():
    with open(XML_FILE, "r", encoding="utf-8") as file:
        data = xmltodict.parse(file.read())

    # Extract key elements
    mod_desc = data.get("modDesc", {})
    version = mod_desc.get("version", "N/A")
    author = mod_desc.get("author", "N/A")
    title = mod_desc.get("title", {}).get("en", "N/A")
    description = mod_desc.get("description", {}).get("en", "N/A")

    # Strip unnecessary whitespace or newlines from CDATA content
    if isinstance(description, str):
        description = description.strip()

    # Extract detailed sections (vehicles, placeables, etc.) from description
    vehicles_section = description.split("Vehicles:")[1].split("Placeables:")[0].strip() if "Vehicles:" in description else ""
    placeables_section = description.split("Placeable items:")[1].split("Script Mods:")[0].strip() if "Placeable items:" in description else ""
    script_mods_section = description.split("Script Mods:")[1].split("Mod Dependencies:")[0].strip() if "Script Mods:" in description else ""
    dependencies_section = description.split("Mod Dependencies:")[1].strip() if "Mod Dependencies:" in description else ""

    # Format extracted data
    content = f"""
# {title}

**Version:** {version}  
**Author:** {author}  

## Description

{description.split("Vehicles:")[0].strip()}

### Vehicles
{vehicles_section}

### Placeables
{placeables_section}

### Script Mods
{script_mods_section}

### Mod Dependencies
{dependencies_section}
"""
    return content

def update_readme(content):
    with open(README_FILE, "w", encoding="utf-8") as readme:
        readme.write(content)

if __name__ == "__main__":
    readme_content = extract_data()
    update_readme(readme_content)
