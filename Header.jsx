import React from "react";
import logo from "../assets/logo.png"; // your logo in src/assets/logo.png

function Header() {
  return (
    <header style={{
      display: "flex",
      alignItems: "center",
      padding: "1rem 2rem",
      backgroundColor: "#111",
      boxShadow: "0 0 20px #2563eb22"
    }}>
      <img 
        src={logo} 
        alt="FakeDeepDetect Logo" 
        style={{ height: "120px",width: "120px", marginRight: "1rem" }} 
      />
     <h1
  style={{
    fontFamily: "'Inter', sans-serif",
    textAlign: "left",            // align left
    fontSize: "3.2rem",
    fontWeight: "bold",
    background: "linear-gradient(90deg, #1e3a8a, #3b82f6, #06b6d4)", // gradient blue tones
    WebkitBackgroundClip: "text",
    color: "transparent",
    margin: 0,
    padding: "1rem 0 0 1rem"
  }}
>Fake News & Deepfake Detection System
</h1>



    </header>
  );
}

export default Header;
