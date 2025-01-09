# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from ner import perform_ner_based_on_language
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask with Nginx!"

@app.route('/ner/get', methods=['GET'])
def ner_get():
    data = { }

    text_query = request.args.get('text', '')  # Default empty string if no query

    # Perform NER
    data = perform_ner_based_on_language(text_query)
    return jsonify(data)

@app.route('/ner/test')
def ner_test():
    data = { }

    text1 = "การประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 วันพุธที่ 18 ธันวาคม 2567 เวลา 09.00 น. ศูนย์ช่วยเหลือสังคม สายด่วน 1300 ดำเนินการจัดประชุมคณะกรรมการพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมในกรุงเทพมหานคร ครั้งที่ 10/2567 เพื่อพิจารณาให้ความช่วยเหลือผู้ประสบปัญหาทางสังคมจำนวน 200 ราย รายละ 3,000 บาท รวมเป็นเงินทั้งสิ้น 600,000 บาท โดยนายอนุรักษ์ มะลิวัลย์ ผู้อำนวยการกองตรวจราชการ เป็นประธาน ณ ห้องประชุมสหวิชาชีพ ศูนย์ช่วยเหลือสังคม ชั้น 1 อาคารกรมพัฒนาสังคมและสวัสดิการ"
    text2 = "The 10th Meeting of the Committee for Social Assistance in Bangkok for the Year 2567 will be held on Wednesday, December 18, 2024, at 9:00 AM. The Social Assistance Center, Hotline 1300, will organize this meeting to consider providing assistance to 200 individuals facing social problems, with each receiving 3,000 THB, totaling 600,000 THB. The meeting will be chaired by Mr. Anurak Maliwan, Director of the Inspection Division, at the Multidisciplinary Meeting Room, Social Assistance Center, 1st Floor, Department of Social Development and Welfare Building."

    # Perform NER
    data = perform_ner_based_on_language(text1)
    return jsonify(data)

if __name__ == '__main__':
    app.run()