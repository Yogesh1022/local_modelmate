// src/auth/Login.jsx

import React, { useState } from "react";
import { login } from "../api/api";
import "../styles/global.css";

import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import ModelMateLogo from "./ModelMateLogo";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/login", {
        email: form.email,
        password: form.password,
      });

      if (response.data.success) {
        setMessage("✅ Login successful. Redirecting...");
        setTimeout(() => navigate("/dashboard"), 1500);
      } else {
        setMessage(response.data.message || "Invalid email or password");
      }
    } catch (error) {
      setMessage("❌ Error logging in");
    }
  };

  const handleGoogleLogin = () => {
    window.open("http://localhost:8000/auth/google", "_self"); // adjust your backend OAuth URL
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
      {/* Logo */}
      <header className="flex flex-col items-center mb-6 animate-fadeIn">
        <ModelMateLogo className="w-20 h-20 mb-2 drop-shadow" />
        {/* <h1 className="text-3xl md:text-4xl font-bold text-white">Welcome to ModelMate</h1> */}
      </header>

      {/* Login Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-white/90 backdrop-blur p-8 rounded-2xl shadow-lg max-w-screen max-h-md animate-fadeIn"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center text-gray-800">Login</h2>

        <input
          name="email"
          type="email"
          onChange={handleChange}
          value={form.email}
          placeholder="Email"
          className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
          required
        />
        <input
          name="password"
          type="password"
          onChange={handleChange}
          value={form.password}
          placeholder="Password"
          className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-100 text-black py-3 rounded hover:bg-blue-500 transition font-semibold"
        >
          Log In
        </button>

        {message && (
          <p className="mt-4 text-center text-sm text-red-600">{message}</p>
        )}

        <div className="mt-4 text-center text-gray-700">
          Don’t have an account?{" "}
          <Link to="/signup" className="text-blue-700 hover:underline font-medium">
            Sign up
          </Link>
        </div>

        {/* Divider */}
        <div className="flex items-center my-4">
          <div className="flex-grow h-px bg-gray-300"></div>
          <span className="mx-2 text-gray-500 text-sm">or</span>
          <div className="flex-grow h-px bg-gray-300"></div>
        </div>

        {/* Google OAuth */}
        <button
          type="button"
          onClick={handleGoogleLogin}
          className="w-full flex items-center justify-center gap-2 bg-white border border-gray-300 text-gray-700 py-3 rounded hover:bg-gray-100 transition shadow"
        >
          <img
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
            alt="Google Logo"
            className="w-5 h-5"
          />
          Continue with Google
        </button>

        {/* Back button */}
      <button
        onClick={() => navigate("/")}
        className="absolute bottom-1 left-10 text-black hover:underline text-sm font-medium"
      >
        ← Back to Home
      </button>


      </form>      
    </div>
  );
}
