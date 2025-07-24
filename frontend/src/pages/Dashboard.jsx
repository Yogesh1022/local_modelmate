// // frontend/src/pages/Dashboard.jsx
// import React, { useState, useEffect } from "react";
// import { useAppContext } from "../context/useAppContext";

// import PromptInput from "../components/PromptInput";
// import DiagramViewer from "../components/DiagramViewer";
// import Chatbot from "../components/Chatbot";
// import DownloadButton from "../components/DownloadButton";
// import "../styles/global.css";

// function Dashboard() {
//   const { plantUML } = useAppContext();
//   const [showChatbot, setShowChatbot] = useState(false);
//   const [imageBase64, setImageBase64] = useState("");

//   useEffect(() => {
//     const fetchImage = async () => {
//       if (!plantUML) return;

//       try {
//         const res = await fetch("http://localhost:8000/diagram/render", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ plantuml: plantUML }),
//         });

//         const data = await res.json();
//         setImageBase64(data.image_base64);
//       } catch (err) {
//         console.error("Failed to render diagram:", err);
//         setImageBase64("");
//       }
//     };

//     fetchImage();
//   }, [plantUML]);

//   return (
//     <div className="dashboard-container">
//       <h1 className="dashboard-title">📊 Generate Your Diagram</h1>

//       <PromptInput />

//       <div className="diagram-section">
//         {imageBase64 && (
//           <>
//             <img
//               src={`data:image/png;base64,${imageBase64}`}
//               alt="Generated diagram"
//               style={{ maxWidth: "100%", border: "1px solid #ccc", marginBottom: "10px" }}
//             />
//             <DownloadButton imageBase64={imageBase64} />
//           </>
//         )}
//       </div>

//       <div className="chatbot-toggle">
//         <button onClick={() => setShowChatbot(!showChatbot)}>
//           {showChatbot ? "Hide Chatbot 🤖" : "Ask Assistant 💬"}
//         </button>
//       </div>

//       {showChatbot && <Chatbot />}
//     </div>
//   );
// }

// export default Dashboard;



import React, { useState, useContext, useEffect } from 'react';
import { AppContext } from '../context/AppContext';
import { Bot, BrainCircuit, PenSquare, Search, Send, FileClock } from 'lucide-react';
import { processPrompt, fetchHistory } from '../api/api'; // Make sure to add processPrompt to api.js

const Dashboard = () => {
  const { user } = useContext(AppContext);
  const [prompt, setPrompt] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    // Fetch recent user activity when the component mounts
    const loadHistory = async () => {
      try {
        const historyData = await fetchHistory(); // Assuming fetchHistory gets the last few items
        // Get the last 3 unique prompts
        const uniquePrompts = [...new Map(historyData.history.map(item => [item.prompt, item])).values()];
        setRecentActivity(uniquePrompts.slice(0, 3));
      } catch (error) {
        console.error("Failed to fetch recent activity:", error);
      }
    };
    loadHistory();
  }, []);


  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const newUserMessage = {
      role: 'user',
      content: prompt,
    };

    setChatHistory(prev => [...prev, newUserMessage]);
    setPrompt('');
    setIsBotTyping(true);

    try {
      // Call the backend with the prompt and a specific type for project planning
      const response = await processPrompt(prompt, 'project_planning');
      
      const botResponse = {
        role: 'bot',
        content: response.data,
      };
      
      // Simulate typing effect
      setTimeout(() => {
        setChatHistory(prev => [...prev, botResponse]);
        setIsBotTyping(false);
      }, 1000);

    } catch (error) {
      const errorResponse = {
        role: 'bot',
        content: "Sorry, I couldn't process that request. Please try again.",
      };
      setTimeout(() => {
        setChatHistory(prev => [...prev, errorResponse]);
        setIsBotTyping(false);
      }, 1000);
      console.error("Error processing prompt:", error);
    }
  };

  const featureCards = [
    { title: "New Diagram", description: "Convert your ideas into UML diagrams.", icon: PenSquare, path: "/diagrams" },
    { title: "Research Agent", description: "Find academic papers and resources.", icon: Search, path: "/research" },
    { title: "Analyze Code", description: "Get insights and generate models from code.", icon: BrainCircuit, path: "/code-analyzer" },
  ];

  return (
    <div className="bg-gray-50 min-h-screen p-8">
      <header className="mb-10">
        <h1 className="text-4xl font-bold text-gray-800">Welcome back, {user?.name || 'User'}!</h1>
        <p className="text-gray-500 mt-2">Ready to bring your software ideas to life? Let's get started.</p>
      </header>

      {/* Feature Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        {featureCards.map((card, index) => (
          <div key={index} className="bg-white p-6 rounded-2xl shadow-md hover:shadow-lg hover:-translate-y-1 transition-all duration-300 cursor-pointer">
            <card.icon className="w-12 h-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-800">{card.title}</h3>
            <p className="text-gray-500 mt-1">{card.description}</p>
          </div>
        ))}
      </section>
      
      {/* Recent Activity */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center"><FileClock className="w-6 h-6 mr-3 text-gray-500"/>Recent Activity</h2>
         <div className="bg-white p-6 rounded-2xl shadow-md">
           {recentActivity.length > 0 ? (
            <ul className="space-y-4">
              {recentActivity.map((activity, index) => (
                <li key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <p className="text-gray-700 truncate">{activity.prompt}</p>
                  <span className="text-xs text-gray-400">{new Date(activity.timestamp).toLocaleDateString()}</span>
                </li>
              ))}
            </ul>
           ) : (
            <p className="text-center text-gray-500 py-4">No recent activity to show.</p>
           )}
        </div>
      </section>


      {/* Project Planning Chatbot */}
      <section>
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center"><Bot className="w-7 h-7 mr-3 text-gray-500"/> Project Planning Assistant</h2>
        <div className="bg-white rounded-2xl shadow-md">
          <div className="p-6 h-96 overflow-y-auto flex flex-col space-y-4">
            {/* Initial welcome message */}
            {chatHistory.length === 0 && !isBotTyping && (
                 <div className="flex items-start gap-3">
                    <div className="bg-blue-600 p-2 rounded-full text-white"><Bot size={20} /></div>
                    <div className="bg-gray-100 p-4 rounded-lg rounded-tl-none">
                        <p className="text-gray-800">
                            Hello! Describe your project, and I'll help you create a comprehensive plan. For example, "a mobile app for a local library".
                        </p>
                    </div>
                </div>
            )}
            
            {/* Chat Messages */}
            {chatHistory.map((msg, index) => (
              <div key={index} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                {msg.role === 'bot' && <div className="bg-blue-600 p-2 rounded-full text-white flex-shrink-0"><Bot size={20} /></div>}
                <div className={`p-4 rounded-lg max-w-2xl whitespace-pre-wrap ${msg.role === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-gray-100 text-gray-800 rounded-tl-none'}`}>
                  {msg.content}
                </div>
              </div>
            ))}
             {isBotTyping && (
                <div className="flex items-start gap-3">
                    <div className="bg-blue-600 p-2 rounded-full text-white"><Bot size={20} /></div>
                    <div className="bg-gray-100 p-4 rounded-lg rounded-tl-none">
                        <div className="typing-indicator">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                </div>
            )}
          </div>
          <form onSubmit={handleSendMessage} className="p-4 border-t flex items-center gap-4">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Tell me about your project..."
              className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300"
              disabled={isBotTyping}
            >
              <Send />
            </button>
          </form>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;

