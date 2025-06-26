from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import auth, diagram, history, chatbot, research

app = FastAPI(
    title="ModelMate API",
    description="Your Ultimate Guide to Software Modeling",
    version="1.0.0"
)

# CORS Middleware — allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(diagram.router, prefix="/diagram", tags=["Diagram"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(research.router, prefix="/research", tags=["Research"])

# ✅ Health Check Route
@app.get("/")
def read_root():
    return {"message": "🚀 ModelMate Backend is running!"}
