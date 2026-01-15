###### app.py - Complete FastAPI 


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import time
import os
import sys

# Add for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="🤖 Medical ChatAPP API",
    description="Medical ChatAPP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
    print("=" * 50)
    print("🚀 Starting Medical ChatAPP Server...")
    
    try:
        from project.pipeline import main_pipeline
        chatbot = main_pipeline()
        print("✅ Chatbot loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load chatbot: {e}")
        print("💡 Make sure you ran: python build_vector_store.py")
        chatbot = None
    
    print(f"🌐 Server: http://localhost:8001")
    print(f"📚 Docs:   http://localhost:8001/docs")
    print(f"💬 Chat:   http://localhost:8001/chat")
    print("=" * 50)

# ---------------------------
# ROUTES
# ---------------------------

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with chat interface"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Medical ChatAPP</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #0f172a;
                color: white;
            }
            .header {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .chat-box {
                border: 1px solid #334155;
                padding: 20px;
                border-radius: 10px;
                background: #1e293b;
            }
            input {
                width: 70%;
                padding: 10px;
                background: #0f172a;
                border: 1px solid #475569;
                color: white;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            #response {
                margin-top: 20px;
                padding: 15px;
                background: #0f172a;
                border-radius: 5px;
                min-height: 100px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Medical Chatbot</h1>
            <p>Ask questions about Medical Information</p>
        </div>
        
        <div class="chat-box">
            <input type="text" id="question" placeholder="Ask about Medical..." autocomplete="off">
            <button onclick="ask()">Ask</button>
            
            <div id="response">
                <p>Your response will appear here...</p>
            </div>
        </div>
        
        <script>
            async function ask() {
                const question = document.getElementById('question').value;
                const responseDiv = document.getElementById('response');
                responseDiv.innerHTML = '<em>Thinking...</em>';
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: question})
                    });
                    
                    const data = await response.json();
                    responseDiv.innerHTML = `
                        <strong>Question:</strong> ${question}<br><br>
                        <strong>Answer:</strong> ${data.answer}<br>
                        <small>Time: ${data.processing_time}s</small>
                    `;
                } catch (error) {
                    responseDiv.innerHTML = '<em>Error: ' + error + '</em>';
                }
            }
            
            // Enter key support
            document.getElementById('question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') ask();
            });
        </script>
    </body>
    </html>
    """
    return html

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """Alternative chat page"""
    return await home()

@app.get("/api")
async def api_info():
    """API information"""
    return {
        "name": "Medical ChatAPP API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /api/chat",
            "health": "GET /api/health",
            "docs": "GET /docs"
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
    print("🌐 Starting server on port 8001...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001
    )