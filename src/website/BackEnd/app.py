from flask import Flask, request, jsonify, url_for, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"
    file.save(file_path)
    
    

    print(f"File received: {file.filename}, saved to {file_path}")

    return jsonify({"message": "File uploaded successfully", "filename": file.filename})


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5000, debug=True)