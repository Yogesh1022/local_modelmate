
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../../assets/logo.png";

import {
  ChevronDown,
  // LayoutDashboard,
  Bot,
  BookOpen,
  HelpCircle,
  Phone,
  Lightbulb,
} from "lucide-react";

export default function Home() {
  const navigate = useNavigate();
  const [activeDropdown, setActiveDropdown] = useState(null);

  const toggleDropdown = (section) => {
    setActiveDropdown(activeDropdown === section ? null : section);
  };

  const dropdownItems = {
    solution: [
      "Workflow-Powered Modeling",
      "Student-Focused Interface",
      "Effortless Planning & Visuals",
      "Educational Focus"
    ],
    why: [
      "AI + NLP-Powered Analysis",
      "Diagram Accuracy Boost",
      "Interactive Learning Support",
      "Easy Export for Reports"
    ],
    agent: [
      "Keyword Extraction",
      "Domain Mapping",
      "Guided Suggestions",
      "Project Recommendations"
    ],
    chatbot: [
      "Q&A Support",
      "Academic Help",
      "Fast Model Suggestions",
      "24/7 Learning Buddy"
    ],
    help: [
      "User Manual",
      "FAQ",
      "Live Walkthrough",
      "Video Tutorial"
    ],
    contact: [
      "Email Us",
      "Live Chat",
      "GitHub Community",
      "Feedback Form"
    ],
  };

  return (
    <div className="font-sans text-gray-800 bg-white overflow-x-hidden">

      {/* Navigation Header */}
      <header className="flex items-center justify-between px-8 py-4 shadow fixed w-full z-50 bg-white">
        <div className="flex items-center space-x-3">
          <img src={logo} alt="ModelMate Logo" className="h-10 w-auto " />
        </div>
        <nav className="flex space-x-5">
          {[
           
            { name: "Solution", icon: Lightbulb, key: "solution" },
            { name: "Why ModelMate?", icon: BookOpen, key: "why" },
            { name: "Research Agent", icon: Bot, key: "agent" },
            { name: "Chatbot", icon: Bot, key: "chatbot" },
            { name: "Help", icon: HelpCircle, key: "help" },
            { name: "Contact", icon: Phone, key: "contact" },
          ].map((item) => (
            <div key={item.name} className="relative">
              <button
                onClick={() => toggleDropdown(item.key)}
                className="flex items-center text-gray-700 hover:text-blue-700"
              >
                <item.icon className="w-4 h-4 mr-1" />
                {item.name}
                {item.key && <ChevronDown className="w-3 h-3 ml-1" />}
              </button>
              {activeDropdown === item.key && (
                <div className="absolute top-8 left-0 bg-white border rounded shadow-md z-50 w-60 p-4 text-sm space-y-2">
                  {dropdownItems[item.key].map((info, i) => (
                    <p key={i} className="hover:text-blue-600">• {info}</p>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
        <button
          onClick={() => navigate("/login")}
          className="bg-blue-600 text-black px-5 py-2 rounded hover:bg-blue-700 transition"
        >
          Log In
        </button>
      </header>

      {/* Hero Section */}
      <main className="pt-32">
        <section className="bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 text-white py-24 px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            ModelMate: Your Ultimate Guide to Software Development
          </h1>
          <p className="text-lg md:text-xl max-w-4xl mx-auto mb-8">
            Transform project requirements into professional diagrams using cutting-edge AI/ML & NLP—designed especially for students.
          </p>
          <button
            onClick={() => navigate("/signup")}
            className="bg-white text-blue-700 font-bold py-3 px-10 rounded-full hover:bg-gray-100 transition"
          >
            🚀 Try ModelMate Now
          </button>
        </section>

        {/* Key Benefits Section */}
        <section className="py-20 px-6 bg-gray-50 text-center">
          <h2 className="text-3xl font-bold text-blue-700 mb-6">Why Choose ModelMate?</h2>
          <p className="max-w-5xl mx-auto text-lg mb-12">
            With ModelMate, students enjoy fast, intuitive, and accurate modeling—from flowcharts and class diagrams to use case visualization. AI-driven suggestions, guided prompts, and NLP-enhanced understanding make it a complete learning assistant.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              "Fast diagram creation from plain text",
              "Interactive review and model validation",
              "Student-friendly interface with real-time feedback",
              "Built-in research support and chatbot",
              "Easy export to project reports and presentations",
              "Great for learning, collaboration, and documentation"
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-6 rounded-xl shadow hover:shadow-md transition">
                <p className="text-blue-700 font-medium">✔️ {item}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Diagram Types Section */}
        <section className="py-20 px-6 bg-white text-center">
          <h2 className="text-3xl font-bold text-blue-700 mb-6">📊 Diagrams You Can Generate</h2>
          <p className="max-w-4xl mx-auto text-lg mb-10">
            ModelMate helps you convert your requirements into the following system diagrams, useful for every stage of your project lifecycle.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              { title: "Class Diagram", desc: "Shows the classes, attributes, methods, and relationships in object-oriented systems." },
              { title: "Use Case Diagram", desc: "Visualizes system functionality and interactions between users (actors) and the system." },
              { title: "Sequence Diagram", desc: "Depicts object interactions arranged in a time sequence, emphasizing message flow." },
              { title: "Flowchart", desc: "Represents workflows or processes to illustrate step-by-step actions or decisions." },
              { title: "ER Diagram", desc: "Models database structures by showing entity relationships and attributes." },
              { title: "Project Timeline", desc: "Estimates project stages and durations from planning to deployment." },
            ].map((diagram, idx) => (
              <div key={idx} className="bg-gray-50 border rounded-lg p-6 shadow text-left hover:shadow-md transition">
                <h3 className="text-xl font-semibold text-blue-700 mb-2">{diagram.title}</h3>
                <p className="text-sm text-gray-700">{diagram.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Project Cost & Timeline Estimator Section */}
        <section className="py-20 px-6 bg-blue-50 text-center">
          <h2 className="text-3xl font-bold text-blue-700 mb-6">💰 Project Flow & Cost Estimation</h2>
          <p className="max-w-3xl mx-auto text-lg mb-10">
            ModelMate intelligently estimates your project workflow, timeline, and development cost using your input and generated models.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              { title: "Estimated Completion Time", desc: "Automatically suggests development phases (planning, designing, coding, testing) with realistic timelines." },
              { title: "Effort Hours Calculation", desc: "Breakdown of hours needed per diagram or system module based on requirement complexity." },
              { title: "Cost Projection (Optional)", desc: "For professionals or freelancers: rough pricing suggestions based on task complexity and effort." }
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-6 rounded-xl shadow-md text-left">
                <h3 className="text-xl font-semibold text-blue-700 mb-2">{item.title}</h3>
                <p>{item.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 py-6 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} ModelMate. Empowering visual learning.
      </footer>
    </div>
  );
}

