from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
import random

app = Flask(__name__)
CORS(app)  # 允许手机APP跨域访问

# 创建“上传文件夹”用来存图
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "服务器已启动！Dermatology API is running."

@app.route('/predict', methods=['POST'])
def predict():
    # 1. 检查是否有图片发过来
    if 'image' not in request.files:
        return jsonify({'error': '没有图片文件'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400

    # 2. 保存图片到服务器（方便你检查图片有没有传成功）
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"received_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # 3. ！！！这里是“模拟推理”，不调用真正的神经网络模型！！！
    #    生成一个 0~1 之间的随机数，假装是预测概率
    simulated_probability = round(random.uniform(0.1, 0.99), 4)
    
    # 4. 返回 JSON 结果给手机
    return jsonify({
        'code': 200,
        'message': '推理模拟成功（模型尚未接入）',
        'prediction': simulated_probability,
        'saved_path': filepath
    })

if __name__ == '__main__':
    # 让服务器在本地 5000 端口运行，手机和电脑连同一个 WiFi 就能访问
    app.run(host='0.0.0.0', port=5000, debug=True)