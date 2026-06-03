import React from "react";

function ResultCard({ result }) {
  return (
    <div className="result-card" style={{
      backgroundColor: "#111",
      border: "1px solid #2563eb",
      borderRadius: "1rem",
      padding: "1rem",
      marginBottom: "1rem",
      boxShadow: "0 0 15px #2563eb44",
      transition: "transform 0.3s ease"
    }}>
      <h3 style={{ color: "#22c55e" }}>Type: {result.type.toUpperCase()}</h3>
      {result.input && <p>Input: {result.input}</p>}
      {result.filename && <p>File: {result.filename}</p>}
      <p style={{ color: "#2563eb", fontWeight: "bold" }}>Prediction: {result.prediction}</p>
      <p style={{ color: "#facc15" }}>Confidence: {result.confidence}</p>
    </div>
  );
}

export default ResultCard;
