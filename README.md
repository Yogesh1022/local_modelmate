# ModelMate

ModelMate is a web application designed to enhance project management and research through AI-driven tools. It integrates an AI-powered chatbot, a research agent, and diagram generation capabilities (class, ER, flowchart, use case, and sequence diagrams) using Together.ai and MongoDB for data storage. The frontend dashboard provides an intuitive interface to access these features, built with HTML, CSS (Tailwind), and plans for React integration.

## Table of Contents
- Features
- Project Structure
- Prerequisites
- Setup Instructions
  - Local Setup
  - Docker Setup
- Running the Application
- Accessing the Dashboard
- API Endpoints
- Environment Variables
- Dependencies
- Contributing
- License

## Features
- **Authentication**: Secure user registration and login with JWT-based authentication using MongoDB.
- **AI Chatbot**: Interact with an AI-powered chatbot via Together.ai for real-time assistance.
- **Research Agent**: Submit queries to retrieve AI-driven research insights, stored in `data/user_research`.
- **Diagram Generation**: Create class, ER, flowchart, use case, and sequence diagrams using Together.ai.
- **Dashboard**: A user-friendly frontend interface (`backend/static/dashboard.html` or `frontend/public/index.html`) for accessing all features.
- **Data Management**: Store project datasets, vector databases, and user research in `data/`.
- **Extensibility**: Modular backend (`modules/`) and frontend (`frontend/src/modules/`) for adding new diagram types.

## Project Structure

ModelMate/
│
├── .gitignore                         # No changes
├── .env                               # ⚠️ UPDATED - new environment variables
├── README.md                          # ⚠️ UPDATED - new setup instructions
├── venv/                              # No changes
│
├── docker/
│   ├── Dockerfile                     # ⚠️ UPDATED - new dependencies
│   ├── frontend.Dockerfile            # No changes
│   └── docker-compose.yml             # ⚠️ UPDATED - MongoDB service
│
├── data/
│   ├── project_dataset/
│   │   └── academic_projects.json     # No changes
│   ├── vector_db/
│   │   └── index.faiss                # No changes
│   └── user_research/                 # 🆕 NEW DIRECTORY - for JSON storage
│
├── backend/
│   ├── main.py                        # ⚠️ UPDATED - MongoDB connection
│   ├── config.py                      # ⚠️ UPDATED - new settings
│   ├── requirements.txt               # ⚠️ UPDATED - new dependencies
│   │
│   ├── api/
│   │   ├── auth.py                    # ⚠️ UPDATED - MongoDB auth
│   │   ├── project_input.py           # ⚠️ UPDATED - Together.ai integration
│   │   ├── history.py                 # No changes
│   │   ├── research.py                # 🆕 NEW FILE - search/research endpoints
│   │   ├── chatbot.py                 # ⚠️ UPDATED - Together.ai integration
│   │   └── docgen.py                  # No changes
│   │
│   ├── models/
│   │   ├── user.py                    # ⚠️ UPDATED - MongoDB models
│   │   ├── auth.py                    # ⚠️ UPDATED - auth models
│   │   ├── project.py                 # No changes
│   │   ├── diagram.py                 # No changes
│   │   ├── history.py                 # No changes
│   │   └── research.py                # No changes
│   │
│   ├── modules/                       # ⚠️ ALL UPDATED - Together.ai integration
│   │   ├── class_diagram/
│   │   │   ├── generator.py           # ⚠️ UPDATED
│   │   │   ├── parser.py              # No changes
│   │   │   └── prompts.py             # No changes
│   │   │
│   │   ├── er_diagram/
│   │   │   ├── generator.py           # ⚠️ UPDATED
│   │   │   ├── parser.py              # No changes
│   │   │   └── prompts.py             # No changes
│   │   │
│   │   ├── flowchart/
│   │   │   ├── generator.py           # ⚠️ UPDATED
│   │   │   ├── parser.py              # No changes
│   │   │   └── prompts.py             # No changes
│   │   │
│   │   ├── usecase_diagram/
│   │   │   ├── generator.py           # ⚠️ UPDATED
│   │   │   ├── parser.py              # No changes
│   │   │   └── prompts.py             # No changes
│   │   │
│   │   ├── sequence_diagram/
│   │   │   ├── generator.py           # ⚠️ UPDATED
│   │   │   ├── parser.py              # No changes
│   │   │   └── prompts.py             # No changes
│   │
│   ├── services/
│   │   ├── nlp_processor.py           # No changes
│   │   ├── llm_router.py              # 🆕 NEW FILE - Together.ai client
│   │   ├── storage.py                 # No changes
│   │   ├── doc_generator.py           # No changes
│   │   ├── file_export.py             # No changes
│   │   ├── vector_search.py           # No changes
│   │   ├── auth_service.py            # ⚠️ UPDATED - MongoDB integration
│   │   └── file_storage.py            # 🆕 NEW FILE - JSON storage option
│   │
│   ├── utils/
│   │   ├── logger.py                  # No changes
│   │   ├── embedding.py               # No changes
│   │   └── validators.py              # No changes
│   │
│   ├── rag_research_agent/
│   │   ├── pipeline.py                # No changes
│   │   ├── retriever.py               # No changes
│   │   ├── indexer.py                 # No changes
│   │   └── llm_agent.py               # ⚠️ UPDATED - Together.ai integration
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   │
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   │
│   │   ├── api/
│   │   │   └── api.js                 # Axios instance
│   │   │
│   │   ├── auth/                      # Login/Logout
│   │   │   ├── Login.jsx
│   │   │   ├── Logout.jsx
│   │   │   └── useAuth.js             # Auth hook (context/localStorage)
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── DownloadButton.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── History.jsx
│   │   │   └── ResearchAgent.jsx
│   │   │
│   │   ├── modules/                   # Diagram Viewer Modules (1-to-1 with backend)
│   │   │   ├── ClassDiagram.jsx
│   │   │   ├── ERDiagram.jsx
│   │   │   ├── Flowchart.jsx
│   │   │   ├── SequenceDiagram.jsx
│   │   │   └── UseCaseDiagram.jsx
│   │   │
│   │   ├── chatbot/
│   │   │   ├── ChatWindow.jsx
│   │   │   └── ChatInput.jsx
│   │   │
│   │   ├── context/
│   │   │   └── AppContext.jsx         # Zustand or React Context
│   │   │
│   │   └── styles/
│   │       └── global.css

## Prerequisites
- Python 3.11+: For backend development.
- Node.js 18+: For frontend development (React, Vite).
- MongoDB: Local or cloud instance for user data and research storage.
- Docker: For containerized deployment (optional).
- Together.ai API Key: Obtain from https://api.together.ai/.

## Setup Instructions

### Local Setup

1. **Clone the Repository**:

   git clone https://github.com/your-repo/modelmate.git cd modelmate

2. **Backend Setup**:
- Create and activate a virtual environment:

  python -m venv venv  .\venv\Scripts\activate  # Windows  source venv/bin/activate  # Linux/Mac
- Install backend dependencies:

  cd backend  pip install -r requirements.txt
- Create `.env` in `backend/`:

  TOGETHER_API_KEY=your-together-ai-api-key  MONGO_URI=mongodb://localhost:27017/modelmate  MONGO_DB_NAME=modelmate  JWT_SECRET=your-secure-jwt-secret-key  JWT_ALGORITHM=HS256  STATIC_DIR=static
Replace `your-together-ai-api-key` with a valid Together AI key and `your-secure-jwt-secret-key` with a secure string (e.g., `openssl rand -hex 32`).

3. **MongoDB Setup**:
- Install and start MongoDB locally:

  mongod
- Or use a cloud MongoDB instance and update `MONGO_URI` in `.env`.

4. **Frontend Setup**:
- Install frontend dependencies:

  cd frontend  npm install
- Start the frontend development server:

  npm run dev

5. **Static Dashboard**:
- Copy `dashboard.html` to `backend/static/`:

  mkdir backend/static  cp frontend/public/index.html backend/static/dashboard.html
- Update `backend/main.py` to serve static files:

  from fastapi.staticfiles import StaticFiles  app.mount("/static", StaticFiles(directory="static"), name="static")

### Docker Setup

1. **Install Docker**:
- Download and install Docker Desktop: https://www.docker.com/products/docker-desktop

2. **Create `docker/Dockerfile`**:

FROM python:3.11-slim WORKDIR /app COPY backend/requirements.txt . RUN pip install --no-cache-dir -r requirements.txt COPY backend/ . EXPOSE 8000 CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

3. **Create `docker/docker-compose.yml`**:

version: '3.8' services: backend: build: context: . dockerfile: docker/Dockerfile ports: - "8000:8000" env_file: - backend/.env depends_on: - mongodb volumes: - ./backend:/app - ./data:/app/data mongodb: image: mongo:latest ports: - "27017:27017" volumes: - mongodb_data:/data/db frontend: build: context: . dockerfile: docker/frontend.Dockerfile ports: - "5173:5173" volumes: - ./frontend:/app volumes: mongodb_data:

4. **Run Docker Compose**:

cd modelmate docker-compose up --build

## Running the Application

1. **Backend**:

cd backend uvicorn main:app --reload
Access at http://127.0.0.1:8000

2. **Frontend**:

cd frontend npm run dev
Access at http://127.0.0.1:5173

3. **Docker**:

docker-compose up
Backend: http://127.0.0.1:8000
Frontend: http://127.0.0.1:5173

## Accessing the Dashboard
- **Static Dashboard**: Open http://127.0.0.1:8000/static/dashboard.html for the HTML/CSS dashboard.
- **React Dashboard**: Open http://127.0.0.1:5173 for the React-based dashboard (after setting up frontend).
- **Features**:
- Navigate via sidebar (Chatbot, Research, Diagrams).
- Toggle dark/light theme.
- Access user profile and logout.
- View recent activity (e.g., generated diagrams, research queries).

## API Endpoints
- **Health Check**: GET /health

curl http://127.0.0.1:8000/health
Response: {"status":"healthy","database":"connected"}

- **Register User**: POST /auth/register

curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'

- **Login**: POST /auth/login

curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass"}'

- **Chatbot**: POST /chatbot/chat

curl -X POST http://127.0.0.1:8000/chatbot/chat -H "Authorization: Bearer " -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Hello!"}],"save_conversation":false}'

- **Research**: POST /research/search

curl -X POST http://127.0.0.1:8000/research/search -H "Authorization: Bearer " -H "Content-Type: application/json" -d '{"query":"AI trends"}'

## Environment Variables
In `backend/.env`:

TOGETHER_API_KEY=your-together-ai-api-key MONGO_URI=mongodb://localhost:27017/modelmate MONGO_DB_NAME=modelmate JWT_SECRET=your-secure-jwt-secret-key JWT_ALGORITHM=HS256 STATIC_DIR=static

## Dependencies
**Backend** (`requirements.txt`):

fastapi==0.115.0 uvicorn==0.30.6 pymongo==4.8.0 python-dotenv==1.0.1 pydantic==2.9.2 passlib[bcrypt]==1.7.4 python-jose[cryptography]==3.3.0 together==1.2.1
\
**Frontend** (`package.json`):\

React, Vite, Tailwind CSS, Axios (see `frontend/package.json`).\

Contributing\

Fork the repository.\
Create a feature branch: `git checkout -b feature/your-feature`\
Commit changes: `git commit -m "Add your feature"`\
Push to the branch: `git push origin feature/your-feature`\
Open a pull request.\

License\
MIT License. See `LICENSE` file for details.
