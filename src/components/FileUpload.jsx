import { useState } from "react";
import axios from "axios";
import { Button, Progress } from "antd";

function FileUpload() {
    const [files, setFile] = useState([]);  
    const [progress, setProgress] = useState({ started: false, pc: 0 });
    const [msg, setMsg] = useState(null);

    function handleFileSelection(files) {
        const jpegFiles = Array.from(files).filter(file => file.type === "image/jpeg");

        if (jpegFiles.length === 0) {
            alert("Please upload at least one jpeg file.");
            return;
        }

        setFile(jpegFiles); // ✅ Store only jpeg files in state
    }

    function handleUpload() {
        if (files.length === 0) {
            setMsg("No jpeg files selected.");
            return;
        }

        const fd = new FormData();
        files.forEach((file, index) => {
            fd.append(`jpegFile${index + 1}`, file);
        });

        setMsg("Uploading...");
        setProgress({ started: true, pc: 0 });

        axios.post("http://httpbin.org/post", fd, {
            onUploadProgress: (progressEvent) => {
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                setProgress(prevState => ({ ...prevState, pc: percentCompleted }));
            },
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
        .then((res) => {
            console.log(res.data)
            setMsg("Uploaded Successfully");

        })
        .catch(() => {
            setMsg("Upload Failed");
        });
    }

    return (
        <div>
            <h3>Upload jpeg Files</h3>

            <input 
                type="file" 
                multiple 
                accept="image/jpeg"
                onChange={(e) => handleFileSelection(e.target.files)} 
            />
            <Button type="primary" onClick={handleUpload}>Upload</Button>

            <br />

            {files.length > 0 && (
                <div style={{ display: "flex", gap: "10px" }}>
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
