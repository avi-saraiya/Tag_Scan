import React from "react";
import DataFetcher from "../hooks/axios";

function TextBlocks(){
    return(
        <div className="point-container">
            <div className="text-container">
                <p> 
                    <DataFetcher/>
                </p>
            </div>
        </div>
    );
}

export default TextBlocks;