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
UPLOAD_FOLDER = output_path + "/videos"
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
    
    results = analyze_video(file_path, output_path)

    print("aksjcaskjcnaskjc")
    print("aksjcaskjcnaskjc")
    print("aksjcaskjcnaskjc")
    
    print(execute( " -- asjcnasljcn"))
        
    print(results)

    print("aksjcaskjcnaskjc")
    print("aksjcaskjcnaskjc")

    print(f"File received: {file.filename}, saved to {file_path}")

    return results


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5000, debug=True)