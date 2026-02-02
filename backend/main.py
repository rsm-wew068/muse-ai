from fastapi import FastAPI, HTTPException, UploadFile, File, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import io
import uuid
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from graph import muse_graph

app = FastAPI(title="Muse.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (Simple for Hackathon)
# session_id -> { "image_data": bytes, "history": [] }
SESSIONS: Dict[str, Dict] = {}

class RefineRequest(BaseModel):
    session_id: str
    feedback: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Muse.AI - Agentic Music Curator"}

@app.post("/analyze-photo")
async def analyze_photo(file: UploadFile = File(...)):
    """
    Starts the refinement loop.
    """
    print(f"Received photo: {file.filename}")
    
    # Read image bytes
    image_data = await file.read()
    
    # Create Session
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "image_data": image_data,
        "iteration": 0
    }
    
    # Run Graph
    initial_state = {
        "image_data": image_data,
        "user_feedback": None,
        "iteration_count": 0
    }
    
    result = muse_graph.invoke(initial_state)
    
    return {
        "status": "success",
        "session_id": session_id,
        "vibe_analysis": result.get("vibe_description"),
        "search_parameters": result.get("search_parameters"),
        "recommendations": result.get("final_recommendations", [])
    }

@app.post("/refine")
async def refine_playlist(request: RefineRequest):
    """
    Feedback loop: Re-runs the agent with user critique.
    """
    session_id = request.session_id
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session expired or not found")
        
    session = SESSIONS[session_id]
    image_data = session["image_data"]
    
    print(f"Refining session {session_id} with feedback: {request.feedback}")
    
    # Run Graph with Feedback
    state = {
        "image_data": image_data,
        "user_feedback": request.feedback,
        "iteration_count": session["iteration"]
    }
    
    result = muse_graph.invoke(state)
    
    # Update session
    session["iteration"] += 1
    
    return {
        "status": "success",
        "session_id": session_id,
        "vibe_analysis": result.get("vibe_description"), # Narrative might change
        "search_parameters": result.get("search_parameters"),
        "recommendations": result.get("final_recommendations", [])
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
