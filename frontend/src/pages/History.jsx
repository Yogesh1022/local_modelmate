// frontend/src/pages/History.jsx
import React, { useEffect, useState } from "react";
import { fetchHistory } from "../api/api";

const History = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("User not authenticated");
      return;
    }
    fetchHistory(token)
      .then((data) => setHistory(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">🕘 Your History</h2>
      {error && <p className="error">{error}</p>}
      {history.length === 0 ? (
        <p>No history found.</p>
      ) : (
              <ul className="history-list">
        {history.map((item, index) => (
          <li key={index} className="history-item">
            <p><strong>Prompt:</strong> {item.prompt}</p>
            <p><strong>Type:</strong> {item.diagram_type}</p>
          </li>
        ))}
      </ul>
      )}
    </div>
  );
};

export default History;
