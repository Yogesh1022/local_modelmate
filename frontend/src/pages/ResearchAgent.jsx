import React, { useState } from "react";
import { searchResearch } from "../api/api"; // ✅ In ResearchAgent.jsx

import "../styles/global.css";

function ResearchAgent() {
  const [prompt, setPrompt] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

 const handleSearch = async () => {
  setError("");
  setResults([]);

  if (!prompt.trim()) {
    setError("Please enter a topic.");
    return;
  }

  try {
    const res = await searchResearch(prompt);
    setResults(res.results);
  } catch (err) {
    console.error("Research Fetch Error:", err); // ✅ Detailed error in console
    setError("Failed to fetch research projects.");
  }
};


  return (
    <div className="research-container">
      <h1 className="research-title">🔍 Research Assistant</h1>
      <div className="search-box">
        <input
          type="text"
          placeholder="Enter topic (e.g., e-commerce, hospital)..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="results">
        {results.map((item, index) => (
          <div className="research-card" key={index}>
            <h3>{item.project_name}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResearchAgent;
