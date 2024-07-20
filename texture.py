import os
from xml.etree import ElementTree as ET

def add_default_color(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Check if a <default> element already exists, if not, create one
    default_element = root.find('default')
    if default_element is None:
        default_element = ET.Element('default')
        root.insert(0, default_element)

    # Add the <geom> element with rgba attribute to the <default> element
    geom_element = ET.Element('geom')
    geom_element.set('rgba', '1 1 1 1')
    default_element.append(geom_element)

    # Save the modified XML back to file
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            add_default_color(file_path)
            print(f"Processed {file_path}")

if __name__ == "__main__":
    folder_path = 'D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-10_15-40-19'  # Replace with your folder path
    process_folder(folder_path)