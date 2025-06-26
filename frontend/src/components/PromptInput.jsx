import React, { useState } from "react";
import { useAppContext } from "../context/useAppContext";
import { generateDiagram } from "../api/api";

const PromptInput = () => {
  const { setDiagramType, setPlantUML } = useAppContext();
  const [prompt, setPrompt] = useState("");
  const [selectedType, setSelectedType] = useState("class");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setLoading(true);

  const token = localStorage.getItem("token");

  try {
    const res = await generateDiagram(prompt, selectedType, token);
    setDiagramType(selectedType);
    setPlantUML(res.plantuml);
  } catch (err) {
    setError(err.message || "Diagram generation failed");
  } finally {
    setLoading(false);
  }
};



  return (
    <div className="prompt-input-container">
      <form className="prompt-form" onSubmit={handleSubmit}>
        <textarea
          className="prompt-textarea"
          placeholder="Describe your project or requirement..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
        />

        <div className="prompt-controls">
          <select
            className="diagram-type-select"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            <option value="class">Class Diagram</option>
            <option value="sequence">Sequence Diagram</option>
            <option value="usecase">Use Case Diagram</option>
          </select>

          <button className="generate-button" type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate Diagram"}
          </button>
        </div>

        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};

export default PromptInput;
