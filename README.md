# TagScan
TagScan - AI-Powered Cloth Tag Reader
This repository contains a Flask backend and a React frontend that work together to process image uploads. The backend receives images from the frontend, processes them, and returns results. The React frontend allows users to select and upload an image, receiving and displaying the backend's response.

## Project Structure

- **Backend (Flask)**:  
  The Flask backend provides an API endpoint (`/process`) that accepts image files, processes them, and returns results.

- **Frontend (React)**:  
  The React frontend allows users to select an image from their local system and send it to the backend for processing.

## Requirements

- Python 3.x
- Node.js (for React frontend)
- Flask
- Flask-CORS (for handling cross-origin requests)
- Axios (for making HTTP requests in React)

### Backend (Flask) Setup

1. Install the required Python dependencies:

   ```bash
   pip install Flask flask-cors
   ```


Run the Flask backend by executing the following:

    ```bash
        python app.py
    ```

The backend will start on http://localhost:5000.

Frontend (React) Setup
Ensure you have Node.js installed. If not, download and install it from here.

Install the necessary frontend dependencies:

    ```bash
        npm install axios
      ```

Start the React development server by running:

```bash
    npm start
```

The frontend will be available at http://localhost:3000.

Backend Details
File Upload Handling:
The Flask backend has an endpoint /process which accepts POST requests with an image file attached. The image is saved to the server in the uploads folder, and the process_image function simulates processing (you can replace this with actual image processing logic as needed).

CORS:
Cross-Origin Resource Sharing (CORS) is enabled to allow the React frontend (running on a different port) to interact with the backend without running into CORS issues.

API Response:
The backend returns a JSON response containing the result of the image processing (currently a message indicating successful image detection).

Backend Code Example:
```python
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import os 
    from egbackendpyfile import process_image

    app = Flask(__name__)
    CORS(app)

    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/process', methods=['POST'])
    def process():
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        
        result = process_image(image_path)
        return jsonify({"result": result})

    if __name__ == '__main__':
        app.run(debug=True)
```

Frontend Details
Image Upload:
The React app includes a simple interface where users can select an image file and upload it to the Flask backend. The uploaded image is sent as a FormData object via a POST request to http://localhost:5000/process.

Displaying Results:
After receiving the response from the backend, the result is displayed on the page.

Frontend Code Example:
```javascript

    import React, { useState } from 'react';
    import axios from 'axios';

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
    }

export default App;
```

How to Use
Start the Flask backend by running python app.py.
Start the React frontend by running npm start.
Open the frontend in your browser (http://localhost:3000).
Select an image file and click "Upload Image."
The result of the image processing (simulated in this example) will be displayed below the button.
Future Enhancements
Image Processing:
Replace the process_image function with actual image processing logic (e.g., integrating Gemini API or other image analysis tools).

Error Handling:
Improve error handling in both the frontend and backend for better user experience and robustness.
