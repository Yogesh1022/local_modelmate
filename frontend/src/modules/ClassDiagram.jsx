// frontend/src/modules/ClassDiagram.jsx
import React from "react";

function ClassDiagram({ plantUml }) {
  if (!plantUml) {
    return <p style={{ color: "#888" }}>No class diagram available.</p>;
  }

  return (
    <div className="diagram-viewer">
      <h2>📘 Class Diagram</h2>
      <pre className="plantuml-code">{plantUml}</pre>
    </div>
  );
}

export default ClassDiagram;
