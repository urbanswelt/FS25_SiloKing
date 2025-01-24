import xml.etree.ElementTree as ET
from lxml import etree
from googletrans import Translator

def translate_moddesc(file_path):
     translator = Translator()
     tree = etree.parse(file_path)
     root = tree.getroot()

     description = root.find(".//description")
     en_description = description.find("en").text

     # Translate English to German
     translated = translator.translate(en_description, src="en", dest="de").text

     # Update <de> description
     de_description = description.find("de")
     if de_description is None:
         de_description = etree.SubElement(description, "de")
     de_description.text = f"<![CDATA[{translated}]]>"

     # Save the updated XML
     tree.write(file_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
     translate_moddesc("modDesc.xml")