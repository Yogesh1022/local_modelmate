import React, { useState } from "react";
import { chatWithBot } from "../api/api";
import "../styles/global.css";

const Chatbot = () => {
  const [message, setMessage] = useState("");
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("token");
const sendMessage = async () => {
  if (!message.trim()) return;

  setLoading(true);
  try {
    const res = await chatWithBot(message, token);
    setResponses((prev) => [
      ...prev,
      { user: message, bot: res.response },  // ✅ Corrected here
    ]);
    setMessage("");
  } catch (err) {
    console.error("Chatbot Error:", err);
    setResponses((prev) => [
      ...prev,
      { user: message, bot: "⚠️ Error reaching chatbot." },
    ]);
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="chatbot-box">
      <h3>🤖 Ask ModelMate Assistant</h3>
      <div className="chatbot-messages">
        {responses.map((pair, index) => (
          <div key={index} className="chat-pair">
            <p><strong>You:</strong> {pair.user}</p>
            <p><strong>Bot:</strong> {pair.bot}</p>
            <hr />
          </div>
        ))}
      </div>

      <div className="chatbot-input">
        <input
          type="text"
          placeholder="Ask anything..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
