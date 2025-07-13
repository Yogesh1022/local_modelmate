import React, { useState } from "react";

import { signup, verifyOtp } from "../api/api";

import { Link, useNavigate } from "react-router-dom";
import ModelMateLogo from "./ModelMateLogo";

export default function Signup() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setMessage("❗ Passwords do not match.");
      return;
    }
    try {
      const response = await signup(formData.name, formData.email, formData.password);
      if (response.success) {
        setOtpSent(true);
        setMessage("✅ OTP sent to your email.");
      } else {
        setMessage(response.message || "Something went wrong.");
      }
    } catch (error) {
      setMessage("❌ Error sending OTP.");
    }
  };

  const handleOtpVerify = async (e) => {
    e.preventDefault();
    try {
      const response = await verifyOtp(formData.email, otp);
      if (response.success) {
        setMessage("✅ Signup successful. Redirecting to login...");
        setTimeout(() => navigate("/login"), 1500);
      } else {
        setMessage("❌ Invalid OTP.");
      }
    } catch (error) {
      setMessage("❌ Error verifying OTP.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
      {/* Header */}
      <header className="flex flex-col items-center mb-6 animate-fadeIn">
        <ModelMateLogo className="w-16 h-16 mb-2" />
        {/* <h1 className="text-3xl font-bold text-blue-700">Welcome to ModelMate</h1> */}
      </header>

      {/* Form */}
      <main className="max-h-screen max-w-md bg-white p-6 rounded-2xl shadow animate-slideUp">
        <h2 className="text-2xl font-semibold mb-4 text-center text-blue-700">
          {otpSent ? "Verify OTP" : "Sign Up"}
        </h2>

        <form onSubmit={otpSent ? handleOtpVerify : handleSignup}>
          {!otpSent && (
            <>
              <input
                type="text"
                name="name"
                placeholder="Name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full p-2 mb-3 border rounded"
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full p-2 mb-3 border rounded"
              />
              <input
                type="password"
                name="password"
                placeholder="Create Password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full p-2 mb-3 border rounded"
              />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full p-2 mb-3 border rounded"
              />
            </>
          )}

          {otpSent && (
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
              className="w-full p-2 mb-3 border rounded"
            />
          )}

          <button
            type="submit"
            className="bg-blue-600 text-black px-4 py-2 rounded hover:bg-blue-700 w-full transition"
          >
            {otpSent ? "Verify OTP" : "Send OTP"}
          </button>
        </form>

        {message && (
          <p className="mt-4 text-center text-sm text-red-600">{message}</p>
        )}

        <div className="mt-4 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 hover:underline">
            Login
          </Link>
        </div>
      </main>
    </div>
  );
}
