// frontend/src/components/DownloadButton.jsx

import React from "react";

const DownloadButton = ({ imageBase64 }) => {
  const handleDownload = () => {
    if (!imageBase64) return;

    const link = document.createElement("a");
    link.href = `data:image/png;base64,${imageBase64}`;
    link.download = "diagram.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <button
      className="download-button"
      onClick={handleDownload}
      disabled={!imageBase64}
    >
      📥 Download PNG
    </button>
  );
};

export default DownloadButton;
