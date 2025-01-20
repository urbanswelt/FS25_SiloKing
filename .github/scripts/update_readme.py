import xmltodict
import markdown

XML_FILE = "modDesc.xml"
README_FILE = "README.md"

def extract_data():
    with open(XML_FILE, "r", encoding="utf-8") as file:
        data = xmltodict.parse(file.read())
    
    mod_desc = data.get("modDesc", {})
    version = mod_desc.get("version", "N/A")
    author = mod_desc.get("author", "N/A")
    title = mod_desc.get("title", {}).get("en", "N/A")
    description = mod_desc.get("description", {}).get("en", "N/A")

    # Format extracted data
    content = f"""
# {title}

**Version:** {version}  
**Author:** {author}  

## Description

{description.strip()}
"""
    return content

def update_readme(content):
    with open(README_FILE, "w", encoding="utf-8") as readme:
        readme.write(content)

if __name__ == "__main__":
    readme_content = extract_data()
    update_readme(readme_content)
