""" TLDR: MODIFY LINE 46 TO TAKE FROM THE ACTUAL BACKEND FILE. 
    ADD THE FOLLOWING FUNCTION TO THE REACT FILE
    function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setResponseMessage('Please select an image to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResponseMessage(response.data.result);
    } catch (error) {
      console.error('Error uploading image:', error);
      setResponseMessage('Error processing image.');
    }
  };

  return (
    <div>
      <h1>Image Upload Processor</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Image</button>
      <p>{responseMessage}</p>
    </div>
  );
}"""

from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS for handling cross-origin requests
import os 
from backend.egbackendpyfile import process_image # This is from the backend file, where the data processing logic is specified

app = Flask(__name__)
CORS(app) # Allows cross-origin requests (React running on a different port)

UPLOAD_FOLDER = 'uploads' # Variable UPLOAD_FOLDER specifies the directory where the uploaded files will be stored, and uploads is the folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # This line makes the uploads folder if it doesn't already exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Stores the path of UPLOAD_FOLDER for later reference

@app.route('/process', methods=['POST']) #Defines a route (like a URL) ending in /process, and accepts a 'POST' request
def process():  #This function will handles the requests that come from the webpage whose URL ends with the /process
    if 'image' not in request.files: # Error handling for it no file is provided
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image'] # Retrieves image from incoming HTTP request
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename) # Created the image file path for storage on the server
    image_file.save(image_path) # Writes the actual image to the specified path
    
    result = process_image(image_path) # Implements the backend logic
    return jsonify({"result": result}) # Returns the result as the value of the 'result' key

# Runs it
if __name__ == '__main__':
    app.run(debug=True)