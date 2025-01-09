# Import required libraries
from langdetect import detect, DetectorFactory
from pythainlp.wangchanberta import ThaiNameTagger
import spacy
import json

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Define mapping for common entity types
COMMON_ENTITY_TYPES = {
    # spaCy mappings
    "PERSON": "PERSON",
    "NORP": "GROUP",
    "FAC": "FACILITY",
    "ORG": "ORGANIZATION",
    "GPE": "LOCATION",
    "LOC": "LOCATION",
    "PRODUCT": "PRODUCT",
    "EVENT": "EVENT",
    "WORK_OF_ART": "WORK_OF_ART",
    "LAW": "LAW",
    "LANGUAGE": "LANGUAGE",
    "DATE": "DATE",
    "TIME": "TIME",
    "PERCENT": "PERCENT",
    "MONEY": "MONEY",
    "QUANTITY": "QUANTITY",
    "ORDINAL": "ORDINAL",
    "CARDINAL": "CARDINAL",

    # WangchanBERTa mappings
    "DATE": "DATE",
    "TIME": "TIME",
    "EMAIL": "EMAIL",
    "LEN": "LENGTH",
    "LOCATION": "LOCATION",
    "ORGANIZATION": "ORGANIZATION",
    "PERSON": "PERSON",
    "PHONE": "PHONE",
    "URL": "URL",
    "ZIP": "ZIP",
    "Money": "MONEY",
    "LAW": "LAW"
}

def map_entity_type(entity_type, model):
    """
    Map the entity type to a common entity type system.

    Args:
        entity_type (str): The original entity type from the model.
        model (str): The name of the model ('spacy' or 'wangchanberta').

    Returns:
        str: The mapped entity type.
    """
    return COMMON_ENTITY_TYPES.get(entity_type, "UNKNOWN")

def unify_entities(entities, model):
    """
    Convert entity types to the common type system.

    Args:
        entities (list): List of entities with 'type' and 'value'.
        model (str): The name of the model ('spacy' or 'wangchanberta').

    Returns:
        list: Entities with mapped types.
    """
    return [{"type": map_entity_type(entity["type"], model), "value": entity["value"]} for entity in entities]

def detect_language(text):
    """
    Detect the language of the given text.

    Args:
        text (str): The input text.

    Returns:
        str: Detected language code (e.g., 'th' for Thai, 'en' for English).
    """
    try:
        return detect(text)
    except:
        return "unknown"

def get_named_entities_thai(text):
    """
    Perform NER on Thai text and group nearby entities of the same type.

    Args:
        text (str): The Thai input text.

    Returns:
        list: Grouped named entities with spaces for DATE and PERSON types.
    """
    # Initialize Thai NER model
    thai_ner = ThaiNameTagger()

    results = thai_ner.get_ner(text)
    grouped_entities = []
    current_group = {"type": None, "value": ""}

    for token, tag in results:
        if tag == "O":  # Ignore tokens outside any named entity
            continue

        entity_type = tag.split('-')[-1]  # Extract type (e.g., DATE, PERSON)
        
        if current_group["type"] == entity_type:
            # Add space before the token for DATE and PERSON
            if entity_type in ["DATE", "PERSON"]:
                current_group["value"] += " " + token
            else:
                current_group["value"] += token
        else:
            if current_group["type"]:
                # Save the previous group if it exists
                grouped_entities.append(current_group)
            # Start a new group
            current_group = {"type": entity_type, "value": token}

    # Add the last group if it exists
    if current_group["type"]:
        grouped_entities.append(current_group)

    return [{"type": entity["type"], "value": entity["value"].strip()} for entity in grouped_entities]

def get_named_entities_english(text):
    """
    Perform NER on English text using spaCy.

    Args:
        text (str): The English input text.

    Returns:
        list: Named entities with their types and values.
    """
    # Initialize spaCy English NER model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [{"type": ent.label_, "value": ent.text} for ent in doc.ents]

def perform_ner_based_on_language(text):
    """
    Perform language detection and NER based on detected language.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary containing the language and grouped named entities.
    """
    language = detect_language(text)
    if language == "th":
        entities = get_named_entities_thai(text)
        unified_entities = unify_entities(entities, "wangchanberta")
    elif language == "en":
        entities = get_named_entities_english(text)
        unified_entities = unify_entities(entities, "spacy")
    else:
        unified_entities = []

    return {"language": language, "entities": unified_entities}

# if __name__ == "__main__":
#     # Input texts
#     text1 = "การประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 วันพุธที่ 18 ธันวาคม 2567 เวลา 09.00 น. ศูนย์ช่วยเหลือสังคม สายด่วน 1300 ดำเนินการจัดประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 เพื่อพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมจำนวน 200 ราย รายละ 3,000 บาท รวมเป็นเงินทั้งสิ้น 600,000 บาท โดยนายอนุรักษ์ มะลิวัลย์ ผู้อำนวยการกองตรวจราชการ เป็นประธาน ณ ห้องประชุมสหวิชาชีพ ศูนย์ช่วยเหลือสังคม ชั้น 1 อาคารกรมพัฒนาสังคมและสวัสดิการ"
#     text2 = "The 10th Meeting of the Committee for Social Assistance in Bangkok for the Year 2567 will be held on Wednesday, December 18, 2024, at 9:00 AM. The Social Assistance Center, Hotline 1300, will organize this meeting to consider providing assistance to 200 individuals facing social problems, with each receiving 3,000 THB, totaling 600,000 THB. The meeting will be chaired by Mr. Anurak Maliwan, Director of the Inspection Division, at the Multidisciplinary Meeting Room, Social Assistance Center, 1st Floor, Department of Social Development and Welfare Building."

#     # Perform NER
#     result1 = perform_ner_based_on_language(text1)
#     # result2 = perform_ner_based_on_language(text2)

#     # Print results as JSON
#     print("Result for Text 1:")
#     print(json.dumps(result1, ensure_ascii=False, indent=4))

#     # print("\nResult for Text 2:")
#     # print(json.dumps(result2, ensure_ascii=False, indent=4))