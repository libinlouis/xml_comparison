import xml.etree.ElementTree as ET
import pandas as pd

attr_mapping = {'LastStatusChange': ''}

def xml_fetch_attributes(xml_source_path):
    # Parse the XML data from the file
    tree = ET.parse(xml_source_path)
    root = tree.getroot()

    # Initialize lists to store extracted data
    attribute_ids = []
    language_ids = []
    attribute_values = []

    # Iterate through the AttributeValues tags
    for attribute_value in root.findall(".//AttributeValue"):
        attribute_id = attribute_value.get("attributeId")
        language_id = attribute_value.get("languageId")
        value = attribute_value.text

        # Append values to respective lists
        attribute_ids.append(attribute_id)
        language_ids.append(language_id)
        attribute_values.append(value)

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'AttributeId': attribute_ids,
        'LanguageId': language_ids,
        'AttributeValue': attribute_values
    })

    # Display the DataFrame
    print(df)
