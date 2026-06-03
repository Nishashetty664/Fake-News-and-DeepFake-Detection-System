import React, { useState } from "react";
import Header from "./components/Header";
import DetectionForm from "./components/DetectionForm";
import ResultCard from "./components/ResultCard";
import "./styles/globals.css";

function App() {
  const [results, setResults] = useState([]);

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f0f0f",
      color: "#f9fafb",
      fontFamily: "'Inter', sans-serif",
      paddingBottom: "2rem"
    }}>
      <Header />

      <main style={{ padding: "2rem", maxWidth: "800px", margin: "0 auto" }}>
        <DetectionForm setResults={setResults} />

        <section style={{ marginTop: "2rem" }}>
          {results.length === 0 && (
            <p style={{ color: "#888", textAlign: "center" }}>
              No results yet. Enter text or upload an image/video.
            </p>
          )}
          {results.map((res, idx) => (
            <ResultCard key={idx} result={res} />
          ))}
        </section>
      </main>
    </div>
  );
}

export default App;
