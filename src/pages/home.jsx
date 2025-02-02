import React from "react";
import {useNavigate} from "react-router-dom";
import FileUpload from "../components/FileUpload";
import { Button } from "antd";

function Home(){
    const navigate = useNavigate();

    return (
      <div className="App">
        <header className="App-header">
            <img src="https://www.permanentstyle.com/wp-content/uploads/2021/04/hang-up-vintage-london-580x464.jpg"
                width={450} alt = "Clothes.png"
            />
            <h1 className="title">Tag Scanner</h1>
            <div>
                <FileUpload/>
                <Button className = {submitButton? "active": "inactive"} type = "primary" onClick = {() => navigate("/information")}>Submit</Button>
            </div>
        </header>
      </div>
    );
}

export default Home;