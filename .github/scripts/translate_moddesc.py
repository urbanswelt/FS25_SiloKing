import xml.etree.ElementTree as ET
from lxml import etree
from googletrans import Translator

def translate_moddesc(file_path):
    translator = Translator()

    # Parse the XML file using lxml
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Locate the <description> and its <en> tag
    description = root.find(".//description")
    en_description = description.find("en").text.strip()  # Strip unnecessary whitespace

    # Translate English to German
    translated = translator.translate(en_description, src="en", dest="de").text

    # Update <de> description or create it if missing
    de_description = description.find("de")
    if de_description is None:
        de_description = etree.SubElement(description, "de")
    
    # Add CDATA to <de>
    de_description.text = f"<![CDATA[{translated}]]>"

    # Save the updated XML with proper formatting
    tree.write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    translate_moddesc("modDesc.xml")
