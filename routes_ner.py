# -*- coding: utf-8 -*-
# routes/ner_routes.py
from flask import Flask, jsonify, request, Blueprint, render_template
from ner import perform_ner_based_on_language

ner_bp = Blueprint('ner_bp', __name__)

@ner_bp.route('/')
def dashboard():
    return 'ner dashboard '

@ner_bp.route('/test')
def test():
    data = { }

    text1 = "การประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 วันพุธที่ 18 ธันวาคม 2567 เวลา 09.00 น. ศูนย์ช่วยเหลือสังคม สายด่วน 1300 ดำเนินการจัดประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 เพื่อพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมจำนวน 200 ราย รายละ 3,000 บาท รวมเป็นเงินทั้งสิ้น 600,000 บาท โดยนายอนุรักษ์ มะลิวัลย์ ผู้อำนวยการกองตรวจราชการ เป็นประธาน ณ ห้องประชุมสหวิชาชีพ ศูนย์ช่วยเหลือสังคม ชั้น 1 อาคารกรมพัฒนาสังคมและสวัสดิการ"
    text2 = "The 10th Meeting of the Committee for Social Assistance in Bangkok for the Year 2567 will be held on Wednesday, December 18, 2024, at 9:00 AM. The Social Assistance Center, Hotline 1300, will organize this meeting to consider providing assistance to 200 individuals facing social problems, with each receiving 3,000 THB, totaling 600,000 THB. The meeting will be chaired by Mr. Anurak Maliwan, Director of the Inspection Division, at the Multidisciplinary Meeting Room, Social Assistance Center, 1st Floor, Department of Social Development and Welfare Building."

    # Perform NER
    data = perform_ner_based_on_language(text1)
    return jsonify(data)

@ner_bp.route('get', methods=['GET'])
def test_get():
    data = { }

    text_query = request.args.get('text', '')  # Default empty string if no query

    # Perform NER
    data = perform_ner_based_on_language(text_query)
    return jsonify(data)

@ner_bp.route('post', methods=['POST'])
def test_post():
    data = { }

    text_query = request.args.post('text', '')  # Default empty string if no query

    # Perform NER
    data = perform_ner_based_on_language(text_query)
    return jsonify(data)

@ner_bp.route('/text', methods=['POST'])
def text():
    # รับ JSON จากคำขอ
    data = request.get_json()
    
    # ตรวจสอบข้อมูล
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    # ทำบางอย่างกับข้อมูล
    # name = data.get("name", "Unknown")
    # age = data.get("age", "Unknown")
    content = data.get("content", "")

    # Perform NER
    ner = perform_ner_based_on_language(content)

    message = {
        "original_message": content,
        "ner": ner,
    }
    # ส่ง JSON ตอบกลับ
    return jsonify(message)


@ner_bp.route('/form')
def form():
    return render_template('form.html')
