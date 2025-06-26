// frontend/src/context/AppContext.jsx

import React, { createContext, useState } from "react";

export const AppContext = createContext();

export const AppContextProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [diagramType, setDiagramType] = useState("class");
  const [plantUML, setPlantUML] = useState("");

  return (
    <AppContext.Provider
      value={{
        user,
        setUser,
        prompt,
        setPrompt,
        diagramType,
        setDiagramType,
        plantUML,
        setPlantUML,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
