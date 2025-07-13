import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
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
import "./styles/App.css";
import Landing from "./auth/Landing";

// 🧠 Layout wrapper that handles sidebar + navbar
function AppLayout({ children }) {
  return (
    <>
      <Navbar />
      <div className="main-content">
        <Sidebar />
        <div className="page-content">
          {children}
        </div>
      </div>
    </>
  );
}

function App() {
  return (
    <AppContextProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={
              <AppLayout>
                <Dashboard />
              </AppLayout>
            }
          />
          <Route
            path="/research"
            element={
              <AppLayout>
                <ResearchAgent />
              </AppLayout>
            }
          />
          <Route
            path="/history"
            element={
              <AppLayout>
                <History />
              </AppLayout>
            }
          />
          <Route
            path="/chatbot"
            element={
              <AppLayout>
                <Chatbot />
              </AppLayout>
            }
          />
        </Routes>
      </Router>
    </AppContextProvider>
  );
}

export default App;