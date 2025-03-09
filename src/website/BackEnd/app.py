from flask import Flask, request, jsonify, url_for, render_template
from flask_cors import CORS
import os
import sys

# adds the path to main data treatment backend
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
sys.path.insert(0, backend_path)

from executable import analyze_video
from test_backend import execute

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../out"))


app = Flask(__name__)
UPLOAD_FOLDER = output_path
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Create necessary directories
    json_dir = os.path.join(UPLOAD_FOLDER, "json")
    videos_dir = os.path.join(UPLOAD_FOLDER, "videos")
    
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save the file first
    file.save(file_path)
    
    # Check if the file exists after saving it
    if not os.path.exists(file_path):
        return jsonify({"error": "File not saved properly"}), 400

    print(f"File received: {file.filename}, saved to {file_path}", flush=True)

    # Now call your analysis function with the correct parameters
    # Pass the full file path as first argument and output directory as second
    result = analyze_video(file_path, UPLOAD_FOLDER)
    return jsonify(result)


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5000, debug=True)