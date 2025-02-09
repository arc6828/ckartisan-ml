# -*- coding: utf-8 -*-
# routes/routes_nlp.py
from flask import jsonify, request, Blueprint
# from ner import perform_ner_based_on_language
# from pythainlp.tokenize import word_tokenize
from googletrans import Translator
from google.cloud import translate_v2 as translate
client = translate.Client()
#Translator
translator = Translator()

nlp_bp = Blueprint('nlp_bp', __name__)

@nlp_bp.route('/')
def dashboard():
    return 'NLP'


@nlp_bp.route('/translate', methods=['POST'])
async def translate():    
    # text_en = "Hello, how are you?"

    # รับข้อมูลจาก JSON payload หรือ Form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ตรวจสอบข้อมูล
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    # ทำบางอย่างกับข้อมูล
    input = data.get("input", "")

    # translated_text = client.translate(input, target_language="th")
    translation = await translator.translate(input, dest = 'th')
    # print(translated_text["translatedText"])  # สวัสดี, คุณเป็นอย่างไรบ้าง?
    return {
        "input" : input,
        "output" : translation.text,
    }


@nlp_bp.route('/translate/cloud', methods=['POST'])
def translate_cloud():    
    # text_en = "Hello, how are you?"

    # รับข้อมูลจาก JSON payload หรือ Form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ตรวจสอบข้อมูล
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    # ทำบางอย่างกับข้อมูล
    input = data.get("input", "")

    translated_text = client.translate(input, target_language="th")
    # print(translated_text["translatedText"])  # สวัสดี, คุณเป็นอย่างไรบ้าง?
    return {
        "input" : input,
        "output" : translated_text["translatedText"],
    }