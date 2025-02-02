from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
import os

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests (React running on a different port)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['POST'])
def process():
    if 'jpegFile1' not in request.files:
        return jsonify({"error": "No JPEG file provided"}), 400

    uploaded_files = request.files.getlist("jpegFile1")  # Retrieve multiple files
    saved_files = []

    for image_file in uploaded_files:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        saved_files.append(image_path)

    return jsonify({"message": "Files uploaded successfully", "files": saved_files})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows cross-origin requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React frontend requests

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['POST'])
def process():
    if 'jpegFile1' not in request.files:
        return jsonify({"error": "No JPEG file provided"}), 400

    uploaded_files = request.files.getlist("jpegFile1")  # Retrieve multiple files
    saved_files = []

    for image_file in uploaded_files:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        saved_files.append(image_path)

    return jsonify({"message": "Files uploaded successfully", "files": saved_files})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allow connections from other devices
