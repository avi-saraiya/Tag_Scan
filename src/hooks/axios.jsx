import React, { useEffect, useState } from "react";
import axios from "axios";

function DataFetcher(){
    const [message, setMessage] = useState("");
    useEffect(() => {
        async function fetchString(){
            try{
                const response = await axios.get('http://localhost:5000/process-image');
                setMessage(response.data.message);
            } catch (error) {
                console.error("Error fetching string: ", error);
                setMessage("Failed to fetch data"); // ✅ Show error message
            }
        }

        fetchString();
    }, []);

    return (
        <div>
            <p> {message} </p>
        </div>
    );
}

export default DataFetcher;