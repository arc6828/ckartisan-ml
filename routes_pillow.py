from flask import Flask, request, jsonify, send_file, Blueprint, url_for
from PIL import Image, UnidentifiedImageError
import pillow_heif
import os
from io import BytesIO

# app = Flask(__name__)
photo = Blueprint('photo', __name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@photo.route('/')
def index():
    return '''
    <h2>Upload HEIC file to convert to JPG</h2>
    <form method="POST" action="upload" enctype="multipart/form-data">
        <input type="file" name="file" accept=".heic">
        <input type="submit" value="Upload and Convert">
    </form>
    '''

@photo.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save uploaded HEIC temporarily
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:

        if file and file.filename.lower().endswith('.heic'):      

            

            # Convert HEIC to PIL Image
            heif_file = pillow_heif.read_heif(filepath)

            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw"
            )
        else:
            # ใช้ Pillow สำหรับไฟล์ทั่วไป (PNG, JPG, WEBP, ฯลฯ)
            image = Image.open(filepath)

        # แปลงภาพเป็น RGB เพื่อให้บันทึกเป็น JPEG ได้
        image = image.convert("RGB")

        # Resize — ด้านที่ใหญ่ที่สุดไม่เกิน 512 px        
        MAX_SIZE = 512  # กำหนดขนาดสูงสุดของด้านที่ใหญ่ที่สุด
        image.thumbnail((MAX_SIZE, MAX_SIZE))

        # Convert image -> JPEG -> Save to BytesIO or to disk
        filename = os.path.splitext(file.filename)[0] + ".jpg"
        output_path = os.path.join(
            "static",
            OUTPUT_FOLDER,
            filename
        )
        image.save(output_path, "JPEG")

        # Optional: return as download
        # return send_file(output_path, mimetype='image/jpeg')

        # สร้าง URL ที่เข้าถึงไฟล์ JPEG ได้
        file_url = url_for('static', filename=OUTPUT_FOLDER+"/"+filename, _external=True)

        return jsonify({
            'message': 'File converted successfully',
            'jpeg_url': file_url,
            'size': image.size,
        })
    
    except UnidentifiedImageError:
        return jsonify({'error': 'Unsupported or invalid image file'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # return jsonify({'error': 'File must be in HEIC format'}), 400


# if __name__ == '__main__':
#     app.run(debug=True)
