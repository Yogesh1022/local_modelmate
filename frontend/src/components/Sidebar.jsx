// frontend/src/components/Sidebar.jsx

import React from "react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h2 className="sidebar-title">🧠 ModelMate</h2>
      <nav className="sidebar-nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "sidebar-link active-link" : "sidebar-link"
          }
        >
          📊 Dashboard
        </NavLink>
        <NavLink
          to="/research"
          className={({ isActive }) =>
            isActive ? "sidebar-link active-link" : "sidebar-link"
          }
        >
          📚 Research Papers
        </NavLink>
        <NavLink
          to="/chatbot"
          className={({ isActive }) =>
            isActive ? "sidebar-link active-link" : "sidebar-link"
          }
        >
          🤖 Assistant Bot
        </NavLink>
        <NavLink
          to="/history"
          className={({ isActive }) =>
            isActive ? "sidebar-link active-link" : "sidebar-link"
          }
        >
          🕓 History
        </NavLink>
      </nav>
    </div>
  );
};

export default Sidebar;
