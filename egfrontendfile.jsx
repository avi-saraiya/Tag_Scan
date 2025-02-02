import React, { useState } from 'react';
import axios from 'axios'; //Library used to make HTTP requests

function App() {
  // The 2 consts below are useState hooks (basically, inputData is a variable that'll hold the value entered by the user, response will be the processed data from the backend)
  const [selectedFile, setSelectedFile] = useState(null); // State to hold selected file
  const [responseMessage, setResponseMessage] = useState(''); // State to display the response
  
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
