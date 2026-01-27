from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from vision_agent import VisionAgent
from spotify_client import SpotifyClient
from explainer import TrackExplainer

app = FastAPI(title="Muse.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Muse.AI - Photo to Music"}

vision_agent = VisionAgent()
spotify_client = SpotifyClient()
explainer = TrackExplainer()

@app.post("/analyze-photo")
async def analyze_photo(file: UploadFile = File(...)):
    """
    1. Receive photo upload
    2. Gemini 3 Pro analyzes vibe
    3. Search Spotify for matching tracks
    4. Gemini 3 Flash explains each match
    """
    print(f"Received photo: {file.filename}")
    
    # Read image bytes
    image_data = await file.read()
    
    # Step 1: Analyze photo with Gemini Pro Vision
    vibe_analysis = vision_agent.analyze_image(image_data)
    print(f"Vibe Analysis: {vibe_analysis}")
    
    # Step 2: Search Spotify based on vibe
    tracks = spotify_client.search_tracks(vibe_analysis)
    print(f"Found {len(tracks)} tracks")
    
    # Step 3: Explain each track with Gemini Flash
    recommendations = []
    for track in tracks[:5]:  # Top 5 tracks
        explanation = explainer.explain_match(vibe_analysis, track)
        recommendations.append({
            "track": track,
            "explanation": explanation
        })
    
    return {
        "status": "success",
        "vibe_analysis": vibe_analysis,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
