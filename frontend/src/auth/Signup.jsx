// // import React, { useState } from "react";

// // import { signup, verifyOtp } from "../api/api";
// import React, { useState, useContext } from 'react'; // Import useContext
// import { AppContext } from '../context/AppContext'; // Import your context

// import { Link, useNavigate } from "react-router-dom";
// import ModelMateLogo from "./ModelMateLogo";

// export default function Signup() {
//   const [formData, setFormData] = useState({
//     name: "",
//     email: "",
//     password: "",
//     confirmPassword: "",
//   });
//   const [otpSent, setOtpSent] = useState(false);
//   const [otp, setOtp] = useState("");
//   const [message, setMessage] = useState("");
//   const navigate = useNavigate();

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSignup = async (e) => {
//     e.preventDefault();
//     if (formData.password !== formData.confirmPassword) {
//       setMessage("❗ Passwords do not match.");
//       return;
//     }
//     try {
//       const response = await signup(formData.name, formData.email, formData.password);
//       if (response.success) {
//         setOtpSent(true);
//         setMessage("✅ OTP sent to your email.");
//       } else {
//         setMessage(response.message || "Something went wrong.");
//       }
//     } catch (error) {
//       setMessage("❌ Error sending OTP.");
//     }
//   };

//   const handleOtpVerify = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await verifyOtp(formData.email, otp);
//       if (response.success) {
//         setMessage("✅ Signup successful. Redirecting to login...");
//         setTimeout(() => navigate("/login"), 1500);
//       } else {
//         setMessage("❌ Invalid OTP.");
//       }
//     } catch (error) {
//       setMessage("❌ Error verifying OTP.");
//     }
//   };

//   return (
//     <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
//       {/* Header */}
//       <header className="flex flex-col items-center mb-6 animate-fadeIn">
//         <ModelMateLogo className="w-16 h-16 mb-2" />
//         {/* <h1 className="text-3xl font-bold text-blue-700">Welcome to ModelMate</h1> */}
//       </header>

//       {/* Form */}
//       <main className="max-h-screen max-w-md bg-white p-6 rounded-2xl shadow animate-slideUp">
//         <h2 className="text-2xl font-semibold mb-4 text-center text-blue-700">
//           {otpSent ? "Verify OTP" : "Sign Up"}
//         </h2>

//         <form onSubmit={otpSent ? handleOtpVerify : handleSignup}>
//           {!otpSent && (
//             <>
//               <input
//                 type="text"
//                 name="name"
//                 placeholder="Name"
//                 value={formData.name}
//                 onChange={handleChange}
//                 required
//                 className="w-full p-2 mb-3 border rounded"
//               />
//               <input
//                 type="email"
//                 name="email"
//                 placeholder="Email"
//                 value={formData.email}
//                 onChange={handleChange}
//                 required
//                 className="w-full p-2 mb-3 border rounded"
//               />
//               <input
//                 type="password"
//                 name="password"
//                 placeholder="Create Password"
//                 value={formData.password}
//                 onChange={handleChange}
//                 required
//                 className="w-full p-2 mb-3 border rounded"
//               />
//               <input
//                 type="password"
//                 name="confirmPassword"
//                 placeholder="Confirm Password"
//                 value={formData.confirmPassword}
//                 onChange={handleChange}
//                 required
//                 className="w-full p-2 mb-3 border rounded"
//               />
//             </>
//           )}

//           {otpSent && (
//             <input
//               type="text"
//               placeholder="Enter OTP"
//               value={otp}
//               onChange={(e) => setOtp(e.target.value)}
//               required
//               className="w-full p-2 mb-3 border rounded"
//             />
//           )}

//           <button
//             type="submit"
//             className="bg-blue-600 text-black px-4 py-2 rounded hover:bg-blue-700 w-full transition"
//           >
//             {otpSent ? "Verify OTP" : "Send OTP"}
//           </button>
//         </form>

//         {message && (
//           <p className="mt-4 text-center text-sm text-red-600">{message}</p>
//         )}

//         <div className="mt-4 text-center">
//           Already have an account?{" "}
//           <Link to="/login" className="text-blue-600 hover:underline">
//             Login
//           </Link>
//         </div>
//       </main>
//     </div>
//   );
// }

import React, { useState, useContext } from 'react';
import { Link, useNavigate } from "react-router-dom";

// Import API functions and the global context
import { signup, verifyOtp } from "../api/api";
import { AppContext } from '../context/AppContext';

// Import UI components
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
  // Get the login function from the global context
  const { login } = useContext(AppContext);

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
        setMessage("✅ OTP sent to your email. Please check your inbox.");
      } else {
        setMessage(response.message || "Something went wrong during signup.");
      }
    } catch (error) {
      setMessage("❌ Error sending OTP. Please try again.");
    }
  };

  const handleOtpVerify = async (e) => {
    e.preventDefault();
    try {
      const response = await verifyOtp(formData.email, otp);
      if (response.success && response.token) {
        setMessage("✅ Signup successful! Logging you in...");
        
        // Use the login function from context to set user and token globally
        const user = { name: formData.name, email: formData.email };
        login(user, response.token);
        
        // Redirect to the dashboard after a short delay
        setTimeout(() => navigate("/dashboard"), 1500);
      } else {
        setMessage("❌ Invalid OTP. Please try again.");
      }
    } catch (error) {
      setMessage("❌ Error verifying OTP.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
      <header className="flex flex-col items-center mb-6 animate-fadeIn">
        <ModelMateLogo className="w-16 h-16 mb-2" />
      </header>

      <main className="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg animate-slideUp">
        <h2 className="text-2xl font-semibold mb-6 text-center text-gray-800">
          {otpSent ? "Verify Your Email" : "Create an Account"}
        </h2>

        <form onSubmit={otpSent ? handleOtpVerify : handleSignup}>
          {!otpSent ? (
            <>
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <input
                type="email"
                name="email"
                placeholder="Email Address"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <input
                type="password"
                name="password"
                placeholder="Create Password"
                autoComplete="new-password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                autoComplete="new-password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </>
          ) : (
            <input
              type="text"
              placeholder="Enter 6-digit OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
              className="w-full p-3 mb-4 text-center tracking-widest border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
              maxLength="6"
            />
          )}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
          >
            {otpSent ? "Verify & Sign Up" : "Send OTP"}
          </button>
        </form>

        {message && (
          <p className="mt-4 text-center text-sm font-medium text-gray-700">{message}</p>
        )}

        <div className="mt-6 text-center text-sm">
          <span className="text-gray-700">Already have an account?</span>{" "}
          <Link to="/login" className="text-blue-600 hover:underline font-medium">
            Log In
          </Link>
        </div>
      </main>
    </div>
  );
}
