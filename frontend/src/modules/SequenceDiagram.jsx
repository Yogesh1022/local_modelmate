// frontend/src/modules/SequenceDiagram.jsx
import React from "react";

function SequenceDiagram({ plantUml }) {
  if (!plantUml) {
    return <p style={{ color: "#888" }}>No sequence diagram available.</p>;
  }

  return (
    <div className="diagram-viewer">
      <h2>🔁 Sequence Diagram</h2>
      <pre className="plantuml-code">{plantUml}</pre>
    </div>
  );
}

export default SequenceDiagram;
