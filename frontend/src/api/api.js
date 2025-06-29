const API_BASE_URL = "http://localhost:8000";

// 1. Auth
export async function signup(name, email, password) {
  const res = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
    credentials: "include", // <-- Add this
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Signup failed");
  }

  return res.json();
}

export async function login(email, password) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password }),
    credentials: "include", // <-- Add this
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Login failed");
  }

  return res.json();
}

export async function getCurrentUser() {
  const res = await fetch(`${API_BASE_URL}/auth/me`, {
    credentials: "include", // <-- Add this
  });

  if (!res.ok) {
    throw new Error("Unable to fetch user");
  }

  return res.json();
}

// 2. Diagram Generation (cookie-based)
export const generateDiagram = async (prompt, diagramType) => {
  const res = await fetch("http://localhost:8000/diagram/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt, diagram_type: diagramType }),
    credentials: "include", // <-- Add this
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to generate diagram");
  }

  return res.json();
};

// 3. History (cookie-based)
export async function fetchHistory() {
  const res = await fetch("http://localhost:8000/history/", {
    method: "GET",
    credentials: "include", // <-- Add this
  });

  if (!res.ok) throw new Error("Failed to fetch history");
  return await res.json();
}

// 4. Chatbot (cookie-based)
export async function chatWithBot(message) {
  const res = await fetch(`http://localhost:8000/chatbot/chatbot/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
    credentials: "include", // <-- Add this
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to get bot response");
  }

  return res.json();
}

// 5. Research (no auth needed)
export async function searchResearch(prompt) {
  const res = await fetch(`${API_BASE_URL}/research?prompt=${encodeURIComponent(prompt)}`);

  if (!res.ok) {
    throw new Error("Failed to fetch research data");
  }

  return res.json();
}

export async function renderDiagramImage(plantuml) {
  const res = await fetch("http://localhost:8000/diagram/render", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plantuml }),
    credentials: "include", // <-- Add this (optional, if /render ever needs auth)
  });

  if (!res.ok) {
    throw new Error("Failed to render diagram image");
  }

  return res.json(); // returns { image_base64: "..." }
}