####### index.html
####### style.css

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import time
import os
import sys

# Add for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="🤖 Medical ChatApp",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    processing_time: float
    success: bool

# Global chatbot
chatbot = None

@app.on_event("startup")
def startup():
    """Load chatbot on startup"""
    global chatbot
    print("🚀 Starting ML Chatbot Server...")
    
    try:
        # Try to import pipeline
        try:
            from project.pipeline import main_pipeline
        except ImportError:
            from project.pipeline import main_pipeline
        
        chatbot = main_pipeline()
        print("✅ Chatbot loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load chatbot: {e}")
        chatbot = None
    
    print(f"🌐 Server: http://localhost:8000")
    print(f"📚 API docs: http://localhost:8000/docs")
    print(f"💬 Chat UI: http://localhost:8000/")

# ---------------------------
# SERVE STATIC FILES
# ---------------------------

# Serve static files from fronted folder
frontend_dir = "project/fronted"
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    print(f"✅ Serving frontend from: {frontend_dir}")
    
    @app.get("/", response_class=FileResponse)
    async def serve_frontend():
        """Serve the main chat interface"""
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return FileResponse(os.path.join(frontend_dir, "chat.html"))
else:
    print("⚠️ Frontend folder not found")

# ---------------------------
# API ENDPOINTS
# ---------------------------

@app.get("/api")
async def api_info():
    """API information"""
    return {
        "name": "Medical ChatAPP API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /api/chat",
            "health": "GET /api/health"
        },
        "chatbot_loaded": chatbot is not None
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if chatbot else "degraded",
        "chatbot_loaded": chatbot is not None,
        "timestamp": time.time()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with the ML chatbot"""
    start_time = time.time()
    
    if not chatbot:
        return ChatResponse(
            answer="Chatbot not loaded. Please check server logs.",
            processing_time=time.time() - start_time,
            success=False
        )
    
    try:
        response = chatbot.invoke({"input": request.message})
        return ChatResponse(
            answer=response["answer"],
            processing_time=round(time.time() - start_time, 3),
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)