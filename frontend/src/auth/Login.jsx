// src/auth/Login.jsx

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../api/api";
import "../styles/global.css";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  
const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");

  try {
    const res = await login(email, password);
    localStorage.setItem("token", res.access_token);
    localStorage.setItem("user", JSON.stringify(res.user));
    navigate("/dashboard");
  } catch (err) {
    console.error("Login Error:", err);
    setError(err?.message || "Login failed. Please try again.");
  }
};


  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>Welcome Back 👋</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}

        <p className="redirect-msg">
          Don't have an account?{" "}
          <Link className="link" to="/signup">
            Signup
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
