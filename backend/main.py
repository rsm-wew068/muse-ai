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
    allow_origins=[
        "http://localhost:3000",
        "https://muse-frontend-2vu4yee5ha-uc.a.run.app"
    ],
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

from google.cloud import firestore
import datetime

# Initialize Firestore
try:
    db = firestore.Client(project="muse-agent-app")
    print("🔥 Firestore connected")
except Exception as e:
    print(f"⚠️ Firestore init failed (local?): {e}")
    db = None

def get_liked_tracks():
    if not db:
        return []
    try:
        # Get last 20 likes, ordered by timestamp desc
        docs = db.collection("global_likes") \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .limit(20) \
                 .stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error fetching likes: {e}")
        return []

def save_like(track_data: dict):
    if not db:
        return
    try:
        # Add timestamp
        track_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
        # Use track_id as document ID to prevent duplicates
        db.collection("global_likes").document(track_data['id']).set(track_data)
        print(f"Saved like: {track_data['name']}")
    except Exception as e:
        print(f"Error saving like: {e}")

def get_user_preferences() -> str:
    """Summarize liked tracks for the AI agent."""
    likes = get_liked_tracks()
    if not likes:
        return ""
    
    # Extract artists and implied genres (mock logic for now since we don't have genre in minimal track object)
    artists = set([t.get('artist') for t in likes])
    # Limiting to last 10 likes for context window efficiency
    recent_titles = [t.get('name') for t in likes[-10:]]
    
    summary = f"User likes artists: {', '.join(list(artists)[:5])}. Recently liked songs: {', '.join(recent_titles)}."
    return summary

class LikeRequest(BaseModel):
    track_id: str
    track_name: str
    artist_name: str

@app.post("/like-track")
async def like_track(request: LikeRequest):
    save_like({
        "id": request.track_id,
        "name": request.track_name,
        "artist": request.artist_name
    })
    return {"status": "liked"}

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
    
    # Get user preferences
    prefs = get_user_preferences()
    print(f"Injecting user preferences: {prefs}")

    # Run Graph
    initial_state = {
        "image_data": image_data,
        "user_feedback": None,
        "user_preferences": prefs,
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
    
    # Get user preferences again (in case they liked something mid-session)
    prefs = get_user_preferences()

    # Run Graph with Feedback
    state = {
        "image_data": image_data,
        "user_feedback": request.feedback,
        "user_preferences": prefs,
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

@app.get("/stats")
def get_stats():
    """Returns aggregated user stats from Firestore."""
    likes = get_liked_tracks() # Gets up to 20 currently, maybe bump limit inside get_liked_tracks for better stats
    
    # Calculate top artists
    artist_counts = {}
    for track in likes:
        artist = track.get("artist", "Unknown").split(",")[0].strip()
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        
    sorted_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_artists = [{"name": name, "count": count} for name, count in sorted_artists]
    
    return {
        "total_likes": len(likes),
        "top_artists": top_artists,
        "recent_tracks": likes[:5]
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
