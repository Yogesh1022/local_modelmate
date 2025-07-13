import React from "react";

export default function ModelMateLogo({ className = "w-50 h-auto" }) {
  return (
    <div className="flex items-center space-x-4 select-none">
      {/* 3D-like M with circuit */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 200 200"
        className={className}
      >
        <defs>
          <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2563EB" />
            <stop offset="100%" stopColor="#3B82F6" />
          </linearGradient>
          <filter id="shadow" x="-20%" y="-20%" width="150%" height="150%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" floodColor="#000" floodOpacity="0.2" />
          </filter>
        </defs>
        <circle cx="100" cy="30" r="15" fill="url(#grad)" filter="url(#shadow)" />
        <path
          d="
            M 50 50
            L 50 150
            L 75 150
            L 75 85
            L 100 120
            L 125 85
            L 125 150
            L 150 150
            L 150 50
            L 125 50
            L 100 90
            L 75 50
            Z

            M 100 120
            L 100 160

            M 100 175
            A 10 10 0 1 0 100 155
            A 10 10 0 1 0 100 175
          "
          fill="url(#grad)"
          filter="url(#shadow)"
          stroke="url(#grad)"
          strokeWidth="2"
          strokeLinejoin="round"
        />
      </svg>

      {/* ModelMate Text */}
      <h1
        className="
          text-4xl md:text-5xl font-extrabold
          bg-gradient-to-r from-blue-700 via-blue-500 to-blue-300
          bg-clip-text text-transparent
          drop-shadow-[2px_2px_0px_rgba(0,0,0,0.2)]
          tracking-tight
        "
      >
        ModelMate
      </h1>
    </div>
  );
}
