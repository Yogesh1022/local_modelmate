// src/pages/Home.jsx

import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/global.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container" style={{ textAlign: "center", marginTop: "100px" }}>
      <h1 style={{ fontSize: "3rem", color: "#1976d2" }}>Welcome to ModelMate</h1>
      <p style={{ fontSize: "1.2rem", margin: "20px auto", maxWidth: "600px" }}>
        Your Ultimate Guide to Software Modeling — Easily generate Class, Sequence, and Use Case diagrams from natural language using AI!
      </p>
      <button
        className="generate-button"
        style={{ fontSize: "1.2rem", padding: "12px 30px", marginTop: "30px" }}
        onClick={() => navigate("/login")}
      >
        🚀 Get Started
      </button>
    </div>
  );
};

export default Home;
