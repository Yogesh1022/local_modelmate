const API_BASE_URL = "http://localhost:8000";

// 1. Auth
export async function signup(name, email, password) {
  const res = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
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
  });

  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || "Login failed");
  }

  return res.json();
}

export async function getCurrentUser(token) {
  const res = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error("Unable to fetch user");
  }

  return res.json();
}

// 2. Diagram Generation — ✅ FIXED (removed token + correct field)
export const generateDiagram = async (prompt, diagramType, token) => {
  const res = await fetch("http://localhost:8000/diagram/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,  // ✅ Attach token here
    },
    body: JSON.stringify({ prompt, diagram_type: diagramType }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to generate diagram");
  }

  return res.json();
};


// 3. History (requires token)
export async function fetchHistory(token) {
  const res = await fetch("http://localhost:8000/history/", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`, // ✅ include token
    },
  });

  if (!res.ok) throw new Error("Failed to fetch history");
  return await res.json();
}

// 4. Chatbot (requires token)
export async function chatWithBot(message, token) {
  const res = await fetch(`http://localhost:8000/chatbot/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,  // ✅ Send token here
    },
    body: JSON.stringify({ message }),
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
  });

  if (!res.ok) {
    throw new Error("Failed to render diagram image");
  }

  return res.json(); // returns { image_base64: "..." }
}
