import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./auth/Login";
import Signup from "./auth/Signup";
import Dashboard from "./pages/Dashboard";
import ResearchAgent from "./pages/ResearchAgent";
import History from "./pages/History";
import Chatbot from "./components/Chatbot";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import { AppContextProvider } from "./context/AppContext";
import "./styles/global.css";

// 🧠 Layout wrapper that handles sidebar + navbar
function AppLayout() {
  const location = useLocation();
  const hideLayoutRoutes = ["/", "/login", "/signup"];
  const isLayoutVisible = !hideLayoutRoutes.includes(location.pathname);

  return (
    <>
      {isLayoutVisible && <Navbar />}
      <div className="main-content">
        {isLayoutVisible && <Sidebar />}
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/research" element={<ResearchAgent />} />
            <Route path="/history" element={<History />} />
            <Route path="/chatbot" element={<Chatbot />} />
          </Routes>
        </div>
      </div>
    </>
  );
}

function App() {
  return (
    <AppContextProvider>
      <Router>
        <AppLayout />
      </Router>
    </AppContextProvider>
  );
}

export default App;
