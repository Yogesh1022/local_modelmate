// frontend/src/components/Navbar.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import { useAppContext } from "../context/useAppContext";


const Navbar = () => {
  const navigate = useNavigate();
  const { user, setUser } = useAppContext();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand" onClick={() => navigate("/dashboard")} style={{ cursor: "pointer" }}>
        🧠 ModelMate
      </div>
      <div className="navbar-links">
        {user && (
          <>
            <button className="navbar-link" onClick={() => navigate("/dashboard")}>
              Dashboard
            </button>
            <button className="navbar-link" onClick={() => navigate("/research")}>
              Research
            </button>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
