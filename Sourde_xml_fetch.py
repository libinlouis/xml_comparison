import xml.etree.ElementTree as ET
import pandas as pd
import Excel_conv


call = 'source'
attr_mapping = {'id':'thingProductNo','ReleaseStatus':'thingVersionState','CreatedOn':'thingCreatedOn',
                'CreatedBy':'thingCreatedBy','ChangedOn':'thingLastChangedOn','ChangedBy':'thingLastChangedBy',
                'Keywords':'thingKeywords','CountryAppendix_ProductName':'thingAppendixProdName',
                'MarketingResponsibility':'thingMarketingResponsibility','ShortDescription':'thingShortDescription',
                'Application_Areas':'thingIntendedUseHI','HEX_colour_code':'thingColorDefinition',
                'USP':'thingUSP','Special_Advice':'thingPrecautionsPROD','Instructions_For_Use':'thingInstructionsUsePROD',
                'CE_logo':'thingGraphicCE','CE_logo_number':'thingNotifiedBody','Euronorm_logo':'thingGraphicEN',
                'Instructions_For_Use':'thingInstructionsFoUse','show_PH-value':'thingShowPhValue',
                'ProductInfoSheetNumber':'thingProdInfoSheetNo','Expert-Opinion_And_Information':'thingExpertOpinionInfoProd',
                'Other_Remarks':'thingOtherRemarks','Product_Profile':'thingProductProfile','Footnote':'thingFootnotes',
                'Product_Eyecatcher_Text':'thingEyeEyeCatcher','ProductName':'thingProductnameSAP','ProductName':'thingProductName',
                'Mandatory_Text_Public':'thingMandatorytextPublic','Certificate':'thingCertificates',
                'address_title_1':'thingFooterAdressTitle1','address_title_2':'thingFooterAdressTitle2',
                'address_title_3':'thingFooterAdressTitle3','Product_Data':'thingProductDataInfotext',
                'Identifier':'thingClaimApplicationFieldsApplication','Type_of_test':'thingTypeOfTest',
                'Concentration':'thingClaimApplicationConcentration','ContactTime/Time':'thingClaimApplicationTimeValue',
                'Test_Method':'thingClaimApplicationTestMethod','Norm':'thingClaimApplicationTestMethod',
                'Condition':'thingClaimApplicationOrganicCondition','Fix_or_Min_Temperature':'thingClaimApplicationFixOrMinTemp',
                'Max_Temperature':'thingClaimApplicationMaxTemp','System':'thingSystem','VariantId':'thingMaterialNo',
                'publishValid':'atxpublishvalid','publishWanted':'atxpublishwanted','publishIntended':'atxpublishintended',
                'published':'atxpublished','article_ShortDescription':'thingMaterialDescriptionSap',
                'Accessories':'thingApplicationGuide','Cross-Selling':'thingRelevantProducts','publishValid':'atxpublishvalid',
                'publishWanted':'atxpublishwanted','publishIntended':'atxpublishintended','published':'atxpublished',
                'EnvironmentalInformation':'thingEnvInformation','Quality':'assetMDMQuality','CreatedByHPM':'assetCreatedBy',
                'LastChangedByHPM':'assetChangedBy','Alternative_Text':'assetAlternativeTypeText','Document_Identifier':'assetDocumentIdentifier',
                'Filename':'property_originalfilename','Height_cm':'height','Name':'assetPictureDescriptionsCaption',
                'Library':'thingCategorieOfLibraries','Width_cm':'width'}


def xml_fetch_attributes(xml_source_path, out_filepath):
    # Parse the XML data from the file
    tree = ET.parse(xml_source_path)
    root = tree.getroot()

    # Initialize lists to store extracted data
    attribute_ids = []
    language_ids = []
    attribute_values = []
    publish_ids = []
    publish_lan_ids = []
    publish_attr_val = []

    product_element = root.find(".//Product")

    # Iterate through the AttributeValues tags
    for attribute_value in product_element.findall(".//AttributeValues/AttributeValue"):
        attribute_id = attribute_value.get("attributeId")
        language_id = attribute_value.get("languageId")
        value = attribute_value.text

        # Append values to respective lists
        attribute_ids.append(attribute_id)
        language_ids.append(language_id)
        attribute_values.append(value)

    # Create a DataFrame from the lists
    source_df = pd.DataFrame({
        'attribute_name': attribute_ids,
        'locale': language_ids,
        'value': attribute_values
        })

    publish_df = pd.DataFrame()
    # Iterate through Assortment attributes
    for publish_val in ('publishValid','publishWanted','publishIntended','published'):

        for attribute_value in root.findall(f'.//{publish_val}'):
            attribute_id = publish_val
            language_id = attribute_value.get("languageId")
            value = attribute_value.text

            # Append values to respective lists
            publish_ids.append(attribute_id)
            publish_lan_ids.append(language_id)
            publish_attr_val.append(value)

        tmp_df = pd.DataFrame({
            'attribute_name': publish_ids,
            'locale': publish_lan_ids,
            'value': publish_attr_val
            })

        if not publish_df.empty:
            publish_df = pd.concat([publish_df, tmp_df], ignore_index=True)
        else:
            publish_df = tmp_df

    source_df['attribute_name'] = source_df['attribute_name'].replace(attr_mapping)
    publish_df['attribute_name'] = publish_df['attribute_name'].replace(attr_mapping)
    publish_df['value'] = publish_df['value'].str.strip()
    publish_df['value'] = publish_df['value'].str.upper()

    #append_df = pd.concat([source_df, publish_df], ignore_index=True)
    append_df = source_df

    # Return fetched attribute data to main
    Excel_conv.excel_append(call, append_df, out_filepath)
