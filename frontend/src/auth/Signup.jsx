import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signup } from "../api/api";

const Signup = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await signup(form.name, form.email, form.password);
      localStorage.setItem("token", res.access_token);
      localStorage.setItem("user", JSON.stringify(res.user));
      navigate("/dashboard");
    } catch (err) {
      console.error("Signup Error:", err);
      setError(err?.message || "Signup failed. Please try again.");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>Sign Up 📝</h2>
        <p>Create your ModelMate account</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={form.name}
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />

          <button type="submit">Sign Up</button>
          {error && <p className="error">{error}</p>}
        </form>

        <p className="redirect-msg">
          Already have an account?{" "}
          <Link className="link" to="/login">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
