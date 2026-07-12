from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
import random
from PIL import Image
import hashlib

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "服务器已启动！Dermatology API is running."

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': '没有图片文件'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400

    # 保存图片
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"received_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # ===== 提取图片信息 =====
    img = Image.open(filepath)
    width, height = img.size
    file_size = os.path.getsize(filepath) / 1024  # KB
    file_format = img.format if img.format else "unknown"
    mode = img.mode
    channels = len(img.getbands())
    is_color = channels >= 3
    original_filename = file.filename
    
    # 计算 MD5
    with open(filepath, "rb") as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()
    
    return jsonify({
        'code': 200,
        'message': '图像分析完成',
        'image_width': width,
        'image_height': height,
        'file_size_kb': round(file_size, 2),
        'format': file_format,
        'color_mode': mode,
        'channels': channels,
        'is_color': is_color,
        'original_filename': original_filename,
        'md5': md5_hash,
        'saved_path': filepath
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
