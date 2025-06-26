// frontend/src/modules/UsecaseDiagram.jsx
import React from "react";

function UsecaseDiagram({ plantUml }) {
  if (!plantUml) {
    return <p style={{ color: "#888" }}>No use case diagram available.</p>;
  }

  return (
    <div className="diagram-viewer">
      <h2>🎯 Use Case Diagram</h2>
      <pre className="plantuml-code">{plantUml}</pre>
    </div>
  );
}

export default UsecaseDiagram;
