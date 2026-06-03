import React, { useState } from "react";

function DetectionForm({ setResults }) {
  const [type, setType] = useState("text");
  const [textInput, setTextInput] = useState("");
  const [fileInput, setFileInput] = useState(null);
  const [wordCount, setWordCount] = useState(0);

  // Update word count whenever text changes
  const handleTextChange = (e) => {
    const text = e.target.value;
    setTextInput(text);
    const count = text.trim() ? text.trim().split(/\s+/).length : 0;
    setWordCount(count);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // -------------------- VALIDATION --------------------
    if (type === "text") {
      if (!textInput.trim()) {
        alert("Please enter some text to detect!");
        return;
      }
      if (wordCount < 10) {
        alert(`Text too short! Please enter at least 10 words (Current: ${wordCount} words).`);
        return;
      }
    } else if ((type === "image" || type === "video") && !fileInput) {
      alert(`Please upload a ${type} file to detect.`);
      return;
    }

    // -------------------- REQUEST --------------------
    let url = "";
    let options = {};

    if (type === "text") {
      url = "http://127.0.0.1:8000/predict_text/";
      options = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ text: textInput }),
      };
    } else {
      url =
        type === "image"
          ? "http://127.0.0.1:8000/predict_image/"
          : "http://127.0.0.1:8000/predict_video/";
      const formData = new FormData();
      formData.append("file", fileInput);
      options = { method: "POST", body: formData };
    }

    try {
      const res = await fetch(url, options);
      const data = await res.json();
      setResults((prev) => [data, ...prev]);
    } catch (err) {
      console.error("Error connecting to backend:", err);
      alert("Backend connection failed! Make sure FastAPI is running.");
    }
  };

  const handleClear = () => {
    setTextInput("");
    setFileInput(null);
    setWordCount(0);
    setResults([]); // Clear results as well
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
        backgroundColor: "#0f0f1a",
        padding: "1.5rem",
        borderRadius: "12px",
        boxShadow: "0 0 15px #00ffff",
        color: "#fff",
      }}
    >
      <h2 style={{ textAlign: "center", color: "#00ffff" }}>FakeDeepDetect</h2>

      <label>
        Detection Type:
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          style={{
            marginLeft: "1rem",
            padding: "0.4rem",
            borderRadius: "6px",
            backgroundColor: "#111",
            color: "#0ff",
            border: "1px solid #0ff",
          }}
        >
          <option value="text">Text</option>
          <option value="image">Image</option>
          <option value="video">Video</option>
        </select>
      </label>

      {type === "text" && (
        <>
          <textarea
            placeholder="Enter text here (min 10 words)..."
            value={textInput}
            onChange={handleTextChange}
            rows={5}
            style={{
              padding: "0.5rem",
              borderRadius: "6px",
              backgroundColor: "#111",
              color: "#0ff",
              border: "1px solid #0ff",
              resize: "vertical",
            }}
          />
          <p style={{ color: "#0ff", fontSize: "0.85rem" }}>
            Word count: {wordCount} / 10
          </p>
        </>
      )}

      {(type === "image" || type === "video") && (
        <input
          type="file"
          accept={type === "image" ? "image/*" : "video/*"}
          onChange={(e) => setFileInput(e.target.files[0])}
          style={{
            padding: "0.5rem",
            borderRadius: "6px",
            backgroundColor: "#111",
            color: "#0ff",
            border: "1px solid #0ff",
          }}
        />
      )}

      <div style={{ display: "flex", gap: "0.5rem", justifyContent: "center" }}>
        <button
          type="submit"
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "6px",
            backgroundColor: "#0ff",
            color: "#111",
            fontWeight: "bold",
            border: "none",
            cursor: "pointer",
            boxShadow: "0 0 10px #0ff",
          }}
        >
          Detect
        </button>
        <button
          type="button"
          onClick={handleClear}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "6px",
            backgroundColor: "#ff0055",
            color: "#fff",
            fontWeight: "bold",
            border: "none",
            cursor: "pointer",
            boxShadow: "0 0 10px #ff0055",
          }}
        >
          Clear
        </button>
      </div>
    </form>
  );
}

export default DetectionForm;
