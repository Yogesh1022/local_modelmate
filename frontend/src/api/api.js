// const API_BASE_URL = "http://localhost:8000";

// // 1. Auth
// export async function signup(name, email, password) {
//   const res = await fetch(`${API_BASE_URL}/auth/signup`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ name, email, password }),
//     credentials: "include", // <-- Add this
//   });

//   if (!res.ok) {
//     const data = await res.json();
//     throw new Error(data.detail || "Signup failed");
//   }

//   return res.json();
// }

// export async function verifyOtp(email, otp) {
//   const res = await fetch(`${API_BASE_URL}/auth/verify-otp`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ email, otp }),
//     credentials: "include",
//   });

//   if (!res.ok) {
//     const data = await res.json();
//     throw new Error(data.detail || "OTP verification failed");
//   }

//   return res.json();
// }

// // export async function login(email, password) {
// //   const res = await fetch(`${API_BASE_URL}/auth/login`, {
// //     method: "POST",
// //     headers: { "Content-Type": "application/x-www-form-urlencoded" },
// //     body: new URLSearchParams({ username: email, password }),
// //     credentials: "include", // <-- Add this
// //   });

// //   if (!res.ok) {
// //     const data = await res.json();
// //     throw new Error(data.detail || "Login failed");
// //   }

// //   return res.json();
// // }

// export async function login(email, password) {
//   const res = await fetch(`${API_BASE_URL}/auth/login`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ email, password }),
//     credentials: "include",
//   });

//   if (!res.ok) {
//     const data = await res.json();
//     throw new Error(data.detail || "Login failed");
//   }

//   return res.json();
// }


// export async function getCurrentUser() {
//   const res = await fetch(`${API_BASE_URL}/auth/me`, {
//     credentials: "include", // <-- Add this
//   });

//   if (!res.ok) {
//     throw new Error("Unable to fetch user");
//   }

//   return res.json();
// }

// // 2. Diagram Generation (cookie-based)
// export const generateDiagram = async (prompt, diagramType) => {
//   const res = await fetch("http://localhost:8000/diagram/generate", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ prompt, diagram_type: diagramType }),
//     credentials: "include", // <-- Add this
//   });

//   if (!res.ok) {
//     const error = await res.json();
//     throw new Error(error.detail || "Failed to generate diagram");
//   }

//   return res.json();
// };

// // 3. History (cookie-based)
// export async function fetchHistory() {
//   const res = await fetch("http://localhost:8000/history/", {
//     method: "GET",
//     credentials: "include", // <-- Add this
//   });

//   if (!res.ok) throw new Error("Failed to fetch history");
//   return await res.json();
// }

// // 4. Chatbot (cookie-based)
// export async function chatWithBot(message) {
//   const res = await fetch(`http://localhost:8000/chatbot/chatbot/`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ message }),
//     credentials: "include", // <-- Add this
//   });

//   if (!res.ok) {
//     const error = await res.json();
//     throw new Error(error.detail || "Failed to get bot response");
//   }

//   return res.json();
// }

// // 5. Research (no auth needed)
// export async function searchResearch(prompt) {
//   const res = await fetch(`${API_BASE_URL}/research?prompt=${encodeURIComponent(prompt)}`);

//   if (!res.ok) {
//     throw new Error("Failed to fetch research data");
//   }

//   return res.json();
// }

// export async function renderDiagramImage(plantuml) {
//   const res = await fetch("http://localhost:8000/diagram/render", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ plantuml }),
//     credentials: "include", // <-- Add this (optional, if /render ever needs auth)
//   });

//   if (!res.ok) {
//     throw new Error("Failed to render diagram image");
//   }

//   return res.json(); // returns { image_base64: "..." }
// }





// import axios from 'axios';

// // The base URL for all backend API calls
// const API_BASE_URL = "http://localhost:8000";

// // Create a single axios instance that will be used for all API requests.
// // This is configured to automatically include credentials (like cookies)
// // with every request, which is necessary for your authentication system.
// const api = axios.create({
//   baseURL: API_BASE_URL,
//   withCredentials: true,
// });

// /**
//  * Handles user signup.
//  */
// export async function signup(name, email, password) {
//   try {
//     const response = await api.post('/auth/signup', { name, email, password });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Signup failed');
//   }
// }

// /**
//  * Verifies the user's OTP.
//  */
// export async function verifyOtp(email, otp) {
//   try {
//     const response = await api.post('/auth/verify-otp', { email, otp });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'OTP verification failed');
//   }
// }

// /**
//  * Handles user login.
//  */
// export async function login(email, password) {
//   try {
//     const response = await api.post('/auth/login', { email, password });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Login failed');
//   }
// }

// /**
//  * Fetches the currently authenticated user's data.
//  */
// export async function getCurrentUser() {
//   try {
//     const response = await api.get('/auth/me');
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Unable to fetch user');
//   }
// }

// /**
//  * Sends a prompt to generate a diagram.
//  */
// export const generateDiagram = async (prompt, diagramType) => {
//   try {
//     const response = await api.post('/diagram/generate', { prompt, diagram_type: diagramType });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to generate diagram');
//   }
// };

// /**
//  * Fetches the user's prompt history.
//  */
// export async function fetchHistory() {
//   try {
//     const response = await api.get('/history/');
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to fetch history');
//   }
// }

// /**
//  * Sends a message to the chatbot.
//  */
// export async function chatWithBot(message) {
//   try {
//     const response = await api.post('/chatbot/chatbot/', { message });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to get bot response');
//   }
// }

// /**
//  * Searches for research data. This does not require authentication.
//  */
// export async function searchResearch(prompt) {
//   try {
//     const response = await axios.get(`${API_BASE_URL}/research?prompt=${encodeURIComponent(prompt)}`);
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to fetch research data');
//   }
// }

// /**
//  * Renders PlantUML code into an image.
//  */
// export async function renderDiagramImage(plantuml) {
//   try {
//     const response = await api.post('/diagram/render', { plantuml });
//     return response.data; // Expected to return { image_base64: "..." }
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to render diagram image');
//   }
// }





// import axios from 'axios';

// // The base URL for all backend API calls
// const API_BASE_URL = "http://localhost:8000";

// // Create a single axios instance that will be used for all API requests.
// const api = axios.create({
//   baseURL: API_BASE_URL,
//   withCredentials: true,
// });

// /**
//  * Handles user signup.
//  */
// export async function signup(name, email, password) {
//   try {
//     const response = await api.post('/auth/signup', { name, email, password });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Signup failed');
//   }
// }

// /**
//  * Verifies the user's OTP.
//  */
// export async function verifyOtp(email, otp) {
//   try {
//     const response = await api.post('/auth/verify-otp', { email, otp });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'OTP verification failed');
//   }
// }

// /**
//  * Handles user login.
//  */
// export async function login(email, password) {
//   try {
//     const response = await api.post('/auth/login', { email, password });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Login failed');
//   }
// }

// /**
//  * Fetches the currently authenticated user's data.
//  */
// export async function getCurrentUser() {
//   try {
//     const response = await api.get('/auth/me');
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Unable to fetch user');
//   }
// }

// /**
//  * ✅ NEW: Sends a prompt to the general processing endpoint.
//  * This is used by the dashboard chatbot.
//  */
// export async function processPrompt(prompt, promptType = "general") {
//   try {
//     const response = await api.post('/api/prompt/process', { prompt, prompt_type: promptType });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to process prompt');
//   }
// }

/**
 * Sends a prompt to generate a diagram.
 */
// export const generateDiagram = async (prompt, diagramType) => {
//   try {
//     const response = await api.post('/diagram/generate', { prompt, diagram_type: diagramType });
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to generate diagram');
//   }
// };

import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// ✅ FIX: Add an Axios interceptor to attach the JWT token to every request.
// This runs before any `api.get()` or `api.post()` call.
api.interceptors.request.use(
  (config) => {
    // Get the token from localStorage
    const token = localStorage.getItem('token');
    
    // If the token exists, add it to the Authorization header
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    // Do something with request error
    return Promise.reject(error);
  }
);


/**
 * Handles user signup.
 */
export async function signup(name, email, password) {
  try {
    const response = await api.post('/auth/signup', { name, email, password });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Signup failed');
  }
}

/**
 * Verifies the user's OTP.
 */
export async function verifyOtp(email, otp) {
  try {
    const response = await api.post('/auth/verify-otp', { email, otp });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'OTP verification failed');
  }
}

/**
 * Handles user login.
 */
export async function login(email, password) {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
}

/**
 * Fetches the currently authenticated user's data.
 */
export async function getCurrentUser() {
  try {
    const response = await api.get('/auth/me');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Unable to fetch user');
  }
}

/**
 * Sends a prompt to the general processing endpoint.
 */
export async function processPrompt(prompt, promptType = "general") {
  try {
    const response = await api.post('/api/prompt/process', { prompt, prompt_type: promptType });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to process prompt');
  }
}

// ... all your other API functions remain the same


// ... all your other API functions remain the same

/**
 * Fetches the user's prompt history.
 */
export async function fetchHistory() {
  try {
    const response = await api.get('/history/');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch history');
  }
}

/**
 * Sends a message to the chatbot.
 */
export async function chatWithBot(message) {
  try {
    const response = await api.post('/chatbot/chatbot/', { message });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get bot response');
  }
}

/**
 * Searches for research data. This does not require authentication.
 */
export async function searchResearch(prompt) {
  try {
    const response = await axios.get(`${API_BASE_URL}/research?prompt=${encodeURIComponent(prompt)}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch research data');
  }
}

/**
 * Renders PlantUML code into an image.
 */
export async function renderDiagramImage(plantuml) {
  try {
    const response = await api.post('/diagram/render', { plantuml });
    return response.data; // Expected to return { image_base64: "..." }
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to render diagram image');
  }
}
