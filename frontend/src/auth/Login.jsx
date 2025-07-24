// // src/auth/Login.jsx

// // import React, { useState , useContext} from "react";
// // import {AppContext} from "../context/AppContext"; // import from context
// // import { login } from "../api/api";
// // import "../styles/global.css";

// // import { Link, useNavigate } from "react-router-dom";
// // import axios from "axios";
// // import ModelMateLogo from "./ModelMateLogo";

// // export default function Login() {
// //   const [form, setForm] = useState({ email: "", password: "" });
// //   const [message, setMessage] = useState("");
// //   const navigate = useNavigate();
// //   const { login } = useContext(AppContext); // Get the login function from context

// //   const handleChange = (e) => {
// //     setForm({ ...form, [e.target.name]: e.target.value });
// //   };

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     try {
// //       // const response = await axios.post("http://localhost:8000/auth/login", {
// //       //   email: form.email,
// //       //   password: form.password,
// //       // });
// //       // const response = await axios.post("http://localhost:8000/auth/login", {
// //       //     email: form.email,
// //       //     password: form.password,
// //       // }, {
// //       //   withCredentials: true  // 👈 this sends the access_token cookie
// //       // });
// //       const response = await axios.post("http://localhost:8000/auth/login", {
// //   email: form.email,
// //   password: form.password,
// // }, {
// //   withCredentials: true, // ✅ important to send cookies if any
// //   headers: {
// //     "Content-Type": "application/json"
// //   }
// // });



// //       if (response.data.success) {
// //         setMessage("✅ Login successful. Redirecting...");
// //         setTimeout(() => navigate("/dashboard"), 1500);
// //       } else {
// //         setMessage(response.data.message || "Invalid email or password");
// //       }
// //     } catch (error) {
// //       setMessage("❌ Error logging in");
// //     }
// //   };



// src/auth/Login.jsx

// import React, { useState, useContext } from "react";
// import { Link, useNavigate } from "react-router-dom";

// // Import the login function from your centralized api file
// import { login as apiLogin } from "../api/api";
// import { AppContext } from "../context/AppContext";

// // Import UI Components and Styles
// import ModelMateLogo from "./ModelMateLogo";
// import "../styles/global.css";

// export default function Login() {
//   const [form, setForm] = useState({ email: "", password: "" });
//   const [message, setMessage] = useState("");
//   const navigate = useNavigate();
  
//   // Get the login function from your global context to set the user state
//   const { login } = useContext(AppContext);

//   // ❗ FIX: This function was missing. It updates the state as you type.
//   const handleChange = (e) => {
//     setForm({ ...form, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setMessage(""); // Clear previous messages
//     try {
//       // ✅ IMPROVEMENT: Use the centralized apiLogin function
//       const response = await apiLogin(form.email, form.password);

//       if (response.success) {
//         setMessage("✅ Login successful. Redirecting...");
        
//         // Call the login function from context to update the global state
//         login(response.user, response.token);
        
//         // Redirect to the dashboard
//         setTimeout(() => navigate("/dashboard"), 1500);
//       } else {
//         setMessage(response.message || "Invalid email or password");
//       }
//     } catch (error) {
//       // The error message from api.js will be more specific
//       setMessage(`❌ ${error.message}`);
//     }
//   };

//   const handleGoogleLogin = () => {
//     // Make sure your backend has a /auth/google endpoint configured
//     window.open("http://localhost:8000/auth/google", "_self");
//   };

//   return (
//     <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
//       <header className="flex flex-col items-center mb-6 animate-fadeIn">
//         <ModelMateLogo className="w-20 h-20 mb-2 drop-shadow" />
//       </header>

//       <form
//         onSubmit={handleSubmit}
//         className="bg-white/90 backdrop-blur p-8 rounded-2xl shadow-lg w-full max-w-md animate-fadeIn"
//       >
//         <h2 className="text-2xl font-semibold mb-6 text-center text-gray-800">Login</h2>

//         <input
//           name="email"
//           type="email"
//           onChange={handleChange}
//           value={form.email}
//           placeholder="Email"
//           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
//           required
//         />
//         <input
//           name="password"
//           type="password"
//           onChange={handleChange}
//           value={form.password}
//           placeholder="Password"
//           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
//           required
//         />

//         <button
//           type="submit"
//           className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
//         >
//           Log In
//         </button>

//         {message && (
//           <p className="mt-4 text-center text-sm font-medium">{message}</p>
//         )}

//         <div className="mt-4 text-center text-gray-700">
//           Don’t have an account?{" "}
//           <Link to="/signup" className="text-blue-700 hover:underline font-medium">
//             Sign up
//           </Link>
//         </div>

//         <div className="flex items-center my-4">
//           <div className="flex-grow h-px bg-gray-300"></div>
//           <span className="mx-2 text-gray-500 text-sm">or</span>
//           <div className="flex-grow h-px bg-gray-300"></div>
//         </div>

//         <button
//           type="button"
//           onClick={handleGoogleLogin}
//           className="w-full flex items-center justify-center gap-2 bg-white border border-gray-300 text-gray-700 py-3 rounded hover:bg-gray-100 transition shadow"
//         >
//           <img
//             src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
//             alt="Google Logo"
//             className="w-5 h-5"
//           />
//           Continue with Google
//         </button>

//         <Link
//           to="/"
//           className="absolute bottom-4 left-4 text-white hover:underline text-sm font-medium"
//         >
//           ← Back to Home
//         </Link>
//       </form>
//     </div>
//   );
// }

// // import React, { useState, useContext } from "react";
// // import { Link, useNavigate } from "react-router-dom";

// // // Import the login function from your centralized api file
// // import { login as apiLogin } from "../api/api";
// // import { AppContext } from "../context/AppContext";

// // // Import UI Components and Styles
// // import ModelMateLogo from "./ModelMateLogo";
// // import "../styles/global.css";

// // export default function Login() {
// //   const [form, setForm] = useState({ email: "", password: "" });
// //   const [message, setMessage] = useState("");
// //   const navigate = useNavigate();
  
// //   // Get the login function from your global context to set the user state
// //   const { login } = useContext(AppContext);

// //   // This function updates the state as you type in the input fields.
// //   const handleChange = (e) => {
// //     setForm({ ...form, [e.target.name]: e.target.value });
// //   };

// //   // This function runs when the form is submitted.
// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     setMessage(""); // Clear previous messages
// //     try {
// //       // Use the centralized apiLogin function from api.js
// //       const response = await apiLogin(form.email, form.password);

// //       if (response.success) {
// //         setMessage("✅ Login successful. Redirecting...");
        
// //         // Call the login function from context to update the global state
// //         login(response.user, response.token);
        
// //         // Redirect to the dashboard
// //         setTimeout(() => navigate("/dashboard"), 1500);
// //       } else {
// //         setMessage(response.message || "Invalid email or password");
// //       }
// //     } catch (error) {
// //       // The error message from api.js will be more specific
// //       setMessage(`❌ ${error.message}`);
// //     }
// //   };

// //   const handleGoogleLogin = () => {
// //     // Make sure your backend has a /auth/google endpoint configured
// //     window.open("http://localhost:8000/auth/google", "_self");
// //   };

// //   return (
// //     <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
// //       <header className="flex flex-col items-center mb-6 animate-fadeIn">
// //         <ModelMateLogo className="w-20 h-20 mb-2 drop-shadow" />
// //       </header>

// //       <form
// //         onSubmit={handleSubmit}
// //         className="bg-white/90 backdrop-blur p-8 rounded-2xl shadow-lg w-full max-w-md animate-fadeIn"
// //       >
// //         <h2 className="text-2xl font-semibold mb-6 text-center text-gray-800">Login</h2>

// //         <input
// //           name="email"
// //           type="email"
// //           onChange={handleChange}
// //           value={form.email}
// //           placeholder="Email"
// //           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
// //           required
// //         />
// //         <input
// //           name="password"
// //           type="password"
// //           onChange={handleChange}
// //           value={form.password}
// //           placeholder="Password"
// //           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
// //           required
// //         />

// //         <button
// //           type="submit"
// //           className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
// //         >
// //           Log In
// //         </button>

// //         {message && (
// //           <p className="mt-4 text-center text-sm font-medium">{message}</p>
// //         )}

// //         <div className="mt-4 text-center text-gray-700">
// //           Don’t have an account?{" "}
// //           <Link to="/signup" className="text-blue-700 hover:underline font-medium">
// //             Sign up
// //           </Link>
// //         </div>

// //         <div className="flex items-center my-4">
// //           <div className="flex-grow h-px bg-gray-300"></div>
// //           <span className="mx-2 text-gray-500 text-sm">or</span>
// //           <div className="flex-grow h-px bg-gray-300"></div>
// //         </div>

// //         <button
// //           type="button"
// //           onClick={handleGoogleLogin}
// //           className="w-full flex items-center justify-center gap-2 bg-white border border-gray-300 text-gray-700 py-3 rounded hover:bg-gray-100 transition shadow"
// //         >
// //           <img
// //             src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
// //             alt="Google Logo"
// //             className="w-5 h-5"
// //           />
// //           Continue with Google
// //         </button>

// //         <Link
// //           to="/"
// //           className="absolute bottom-4 left-4 text-white hover:underline text-sm font-medium"
// //         >
// //           ← Back to Home
// //         </Link>
// //       </form>
// //     </div>
// //   );
// // }


// // // import React, { useState, useContext } from "react";
// // // import { Link, useNavigate } from "react-router-dom";

// // // // Import the login function from your centralized api file
// // // import { login as apiLogin } from "../api/api";
// // // import { AppContext } from "../context/AppContext";

// // // // Import UI Components and Styles
// // // import ModelMateLogo from "./ModelMateLogo";
// // // import "../styles/global.css";

// // // export default function Login() {
// // //   const [form, setForm] = useState({ email: "", password: "" });
// // //   const [message, setMessage] = useState("");
// // //   const navigate = useNavigate();
  
// // //   // Get the login function from your global context to set the user state
// // //   const { login } = useContext(AppContext);

// // //   // This function updates the state as you type in the input fields.
// // //   const handleChange = (e) => {
// // //     setForm({ ...form, [e.target.name]: e.target.value });
// // //   };

// //   // This function runs when the form is submitted.
// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     setMessage(""); // Clear previous messages
// //     try {
// //       // Use the centralized apiLogin function from api.js
// //       const response = await apiLogin(form.email, form.password);

// //       if (response.success) {
// //         setMessage("✅ Login successful. Redirecting...");
        
// //         // Call the login function from context to update the global state
// //         login(response.user, response.token);
        
// //         // Redirect to the dashboard
// //         setTimeout(() => navigate("/dashboard"), 1500);
// //       } else {
// //         setMessage(response.message || "Invalid email or password");
// //       }
// //     } catch (error) {
// //       // The error message from api.js will be more specific
// //       setMessage(`❌ ${error.message}`);
// //     }
// //   };

// //   const handleGoogleLogin = () => {
// //     // Make sure your backend has a /auth/google endpoint configured
// //     window.open("http://localhost:8000/auth/google", "_self");
// //   };

// //   return (
// //     <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
// //       <header className="flex flex-col items-center mb-6 animate-fadeIn">
// //         <ModelMateLogo className="w-20 h-20 mb-2 drop-shadow" />
// //       </header>

// //       <form
// //         onSubmit={handleSubmit}
// //         className="bg-white/90 backdrop-blur p-8 rounded-2xl shadow-lg w-full max-w-md animate-fadeIn"
// //       >
// //         <h2 className="text-2xl font-semibold mb-6 text-center text-gray-800">Login</h2>

// //         <input
// //           name="email"
// //           type="email"
// //           onChange={handleChange}
// //           value={form.email}
// //           placeholder="Email"
// //           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
// //           required
// //         />
// //         <input
// //           name="password"
// //           type="password"
// //           onChange={handleChange}
// //           value={form.password}
// //           placeholder="Password"
// //           className="w-full mb-4 p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 text-black placeholder-gray-500"
// //           required
// //         />

// //         <button
// //           type="submit"
// //           className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
// //         >
// //           Log In
// //         </button>

// //         {message && (
// //           <p className="mt-4 text-center text-sm font-medium">{message}</p>
// //         )}

// //         <div className="mt-4 text-center text-gray-700">
// //           Don’t have an account?{" "}
// //           <Link to="/signup" className="text-blue-700 hover:underline font-medium">
// //             Sign up
// //           </Link>
// //         </div>

// //         <div className="flex items-center my-4">
// //           <div className="flex-grow h-px bg-gray-300"></div>
// //           <span className="mx-2 text-gray-500 text-sm">or</span>
// //           <div className="flex-grow h-px bg-gray-300"></div>
// //         </div>

// //         <button
// //           type="button"
// //           onClick={handleGoogleLogin}
// //           className="w-full flex items-center justify-center gap-2 bg-white border border-gray-300 text-gray-700 py-3 rounded hover:bg-gray-100 transition shadow"
// //         >
// //           <img
// //             src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
// //             alt="Google Logo"
// //             className="w-5 h-5"
// //           />
// //           Continue with Google
// //         </button>

// //         <Link
// //           to="/"
// //           className="absolute bottom-4 left-4 text-white hover:underline text-sm font-medium"
// //         >
// //           ← Back to Home
// //         </Link>
// //       </form>
// //     </div>
// //   );
// // }



import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login as apiLogin } from "../api/api";
import { AppContext } from "../context/AppContext";
import ModelMateLogo from "./ModelMateLogo";
import "../styles/global.css";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();
  const { login } = useContext(AppContext);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(""); // Clear previous messages
    try {
      const response = await apiLogin(form.email, form.password);

      if (response.success) {
        setMessage("✅ Login successful. Redirecting...");
        login(response.user, response.token);
        setTimeout(() => navigate("/dashboard"), 1500);
      } else {
        setMessage(response.message || "Invalid email or password");
      }
    } catch (error) {
      setMessage(`❌ ${error.message}`);
    }
  };

  const handleGoogleLogin = () => {
    window.open("http://localhost:8000/auth/google", "_self");
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 px-4 relative">
      <header className="flex flex-col items-center mb-6 animate-fadeIn">
        <ModelMateLogo className="w-20 h-20 mb-2 drop-shadow" />
      </header>

      <form
        onSubmit={handleSubmit}
        className="bg-white/90 backdrop-blur p-8 rounded-2xl shadow-lg w-full max-w-md animate-fadeIn"
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
          className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 transition font-semibold"
        >
          Log In
        </button>

        {message && (
          <p className="mt-4 text-center text-sm font-medium">{message}</p>
        )}

        <div className="mt-4 text-center text-gray-700">
          Don’t have an account?{" "}
          <Link to="/signup" className="text-blue-700 hover:underline font-medium">
            Sign up
          </Link>
        </div>
      </form>
    </div>
  );
}