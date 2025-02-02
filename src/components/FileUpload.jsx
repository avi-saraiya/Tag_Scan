import React, { useState } from "react";
import axios from "axios";
import { Button, Progress } from "antd";
import useSubmitButton from "../hooks/useSubmitButton"; // Hook to enable Submit button

function FileUpload() {
    const [files, setFiles] = useState([]);  
    const [progress, setProgress] = useState({ started: false, pc: 0 });
    const [msg, setMsg] = useState(null);
    const { submitButton, setActive } = useSubmitButton(); // Button state hook

    function handleFileSelection(event) {
        const selectedFiles = event.target.files;
        const jpegFiles = Array.from(selectedFiles).filter(file => file.type === "image/jpeg");

        if (jpegFiles.length === 0) {
            alert("Please upload at least one JPEG file.");
            return;
        }

        setFiles(jpegFiles); // ✅ Store JPEG files in state
        setActive(false); // ✅ Disable submit button until upload completes
    }

    async function handleUpload() {
        if (files.length === 0) {
            setMsg("No JPEG files selected.");
            return;
        }

        const fd = new FormData();
        files.forEach((file, index) => {
            fd.append(`jpegFile${index + 1}`, file);
        });

        setMsg("Uploading...");
        setProgress({ started: true, pc: 0 });

        try {
            const response = await axios.post("http://localhost:5000/process", fd, {
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setProgress(prevState => ({ ...prevState, pc: percentCompleted }));
                },
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            });

            console.log("Upload response:", response.data);
            setMsg("Uploaded Successfully");
            setActive(true); // ✅ Enable the submit button after successful upload
        } catch (error) {
            console.error("Upload failed:", error);
            setMsg("Upload Failed");
            setActive(false); // Keep button disabled if upload fails
        }
    }

    return (
        <div>
            <h3>Upload JPEG Files</h3>

            <div className="input-form">
                <input 
                    type="file" multiple
                    accept="image/jpeg"
                    onChange={handleFileSelection} 
                    style={{ alignContent: "center", justifyContent: "space-around" }}
                />
                <Button type="primary" onClick={handleUpload}>Upload</Button>
            </div>
            
            <br />

            {files.length > 0 && (
                <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
                    {files.map((file, index) => (
                        <img 
                            key={index} 
                            src={URL.createObjectURL(file)} 
                            alt={`Preview ${index + 1}`} 
                            style={{ width: "100px", height: "100px", objectFit: "cover" }} 
                        />
                    ))}
                </div>
            )}

            {progress.started && <Progress percent={progress.pc || 0} status={progress.pc < 100 ? "active" : "success"} />}
            {msg && <span>{msg}</span>}
        </div>
    );
}

export default FileUpload;
