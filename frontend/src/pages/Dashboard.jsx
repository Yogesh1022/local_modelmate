// frontend/src/pages/Dashboard.jsx
import React, { useState, useEffect } from "react";
import { useAppContext } from "../context/useAppContext";

import PromptInput from "../components/PromptInput";
import DiagramViewer from "../components/DiagramViewer";
import Chatbot from "../components/Chatbot";
import DownloadButton from "../components/DownloadButton";
import "../styles/global.css";

function Dashboard() {
  const { plantUML } = useAppContext();
  const [showChatbot, setShowChatbot] = useState(false);
  const [imageBase64, setImageBase64] = useState("");

  useEffect(() => {
    const fetchImage = async () => {
      if (!plantUML) return;

      try {
        const res = await fetch("http://localhost:8000/diagram/render", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ plantuml: plantUML }),
        });

        const data = await res.json();
        setImageBase64(data.image_base64);
      } catch (err) {
        console.error("Failed to render diagram:", err);
        setImageBase64("");
      }
    };

    fetchImage();
  }, [plantUML]);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">📊 Generate Your Diagram</h1>

      <PromptInput />

      <div className="diagram-section">
        {imageBase64 && (
          <>
            <img
              src={`data:image/png;base64,${imageBase64}`}
              alt="Generated diagram"
              style={{ maxWidth: "100%", border: "1px solid #ccc", marginBottom: "10px" }}
            />
            <DownloadButton imageBase64={imageBase64} />
          </>
        )}
      </div>

      <div className="chatbot-toggle">
        <button onClick={() => setShowChatbot(!showChatbot)}>
          {showChatbot ? "Hide Chatbot 🤖" : "Ask Assistant 💬"}
        </button>
      </div>

      {showChatbot && <Chatbot />}
    </div>
  );
}

export default Dashboard;
