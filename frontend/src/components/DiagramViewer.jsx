import React, { useEffect, useState } from "react";
import { useAppContext } from "../context/useAppContext";
import { renderDiagramImage } from "../api/api";

const DiagramViewer = () => {
  const { plantUML } = useAppContext();
  const [imageData, setImageData] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const renderImage = async () => {
      if (!plantUML) return;
      setLoading(true);
      setError("");

      try {
        const res = await renderDiagramImage(plantUML);
        setImageData(res.image_base64);
      } catch (err) {
        setError("Rendering failed");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    renderImage();
  }, [plantUML]);

  if (!plantUML) return null;

  return (
    <div className="diagram-viewer">
      <h3>Generated Diagram</h3>
      {loading && <p>Rendering diagram...</p>}
      {error && <p className="error">{error}</p>}
      {imageData && (
        <img
          src={`data:image/png;base64,${imageData}`}
          alt="Generated Diagram"
          style={{ maxWidth: "100%", border: "1px solid #ccc", padding: "10px" }}
        />
      )}
    </div>
  );
};

export default DiagramViewer;
