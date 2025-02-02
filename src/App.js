import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/home";
import InformationPage from "./pages/information";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/information" element={<InformationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
