from flask import Flask, request, jsonify, url_for, render_template, send_file
from flask_cors import CORS
import os
import sys

# adds the path to main data treatment backend
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))
sys.path.insert(0, backend_path)

from executable import analyze_video

output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../out"))


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
UPLOAD_FOLDER = output_path
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    # Create necessary directory
    json_dir = os.path.join(UPLOAD_FOLDER, "json")
    animations_dir = os.path.join(UPLOAD_FOLDER, "animations")
    
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    if not os.path.exists(animations_dir):
        os.makedirs(animations_dir)
    
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
    
    # Add URLs to access the animation
    if result and "animation_path" in result:
        animation_filename = os.path.basename(result["animation_path"])
        result["animation_url"] = f"/animations/{animation_filename}"
    
    return jsonify(result)

@app.route('/animations/<filename>')
def serve_animation(filename):
    """Serve animation files"""
    animations_dir = os.path.join(UPLOAD_FOLDER, "animations")
    return send_file(os.path.join(animations_dir, filename))

@app.route('/')
def index():
    """Serve a simple HTML page for testing"""
    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=5000, debug=True)