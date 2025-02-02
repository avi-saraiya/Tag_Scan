import React from "react";
import {useNavigate} from "react-router-dom";
import FileUpload from "../components/FileUpload";
import { Button } from "antd";
import useSubmitButton from "../hooks/useSubmitButton";
import TextBlock from "./textblocks";

function Home(){
    const navigate = useNavigate();
    const { submitButton, setActive } = useSubmitButton();


    return (
      <div className="App">
        <header className="App-header">
            <img src="https://www.permanentstyle.com/wp-content/uploads/2021/04/hang-up-vintage-london-580x464.jpg"
                width={450} alt = "Clothes.png"
            />
            <h1 className="title">Tag Scanner</h1>
            <div className = "container">
                <FileUpload/>
                <br/>
                <TextBlock></TextBlock>
                {/*<Button className = {useSubmitButton? "active": "inactive"} type = "primary" onClick = {() => navigate("/information")}>Submit</Button>*/}
            </div>
        </header>
      </div>
    );
}

export default Home;