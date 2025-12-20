from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn
import shutil
from music21 import converter
from generator import MusicGenerator
from agent import MusicAgent
from evaluator import MusicEvaluator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Muse.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MusicAppRequest(BaseModel):
    prompt: str
    duration_seconds: Optional[int] = 30

class MusicGenResponse(BaseModel):
    status: str
    midi_path: Optional[str] = None
    audio_path: Optional[str] = None
    metadata: dict
    evaluation: float # Perplexity or Score

class FeedbackRequest(BaseModel):
    prompt: str
    rating: str

feedback_store = []

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Muse.AI Orchestrator"}

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    print(f"Received Feedback: {request.rating} for '{request.prompt}'")
    feedback_store.append(request.dict())
    return {"status": "recorded"}

agent = MusicAgent()
generator = MusicGenerator()

@app.post("/generate") 
async def generate_music(request: MusicAppRequest):
    print(f"Received prompt: {request.prompt}")
    
    relevant_feedback = [f for f in feedback_store if f['prompt'] in request.prompt or request.prompt in f['prompt']]
    params = agent.analyze_intent(request.prompt, feedback_history=relevant_feedback)
    print(f"Agent Parameters: {params}")
    
    gen_params = {
        "tempo": params.get("tempo", 120),
        "key": params.get("key", "C_Major"),
        "mood": params.get("mood", "Neutral")
    }
    
    # Generate MIDI
    output_filename = "output.mid"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    midi_sys_path = os.path.join(script_dir, output_filename)
    
    generated_path = generator.generate_music_from_params(gen_params, output_path=midi_sys_path)
    
    # Evaluate
    try:
        score = converter.parse(generated_path)
        eval_metrics = MusicEvaluator.evaluate_piece(score)
    except Exception as e:
        print(f"Evaluation Failed: {e}")
        eval_metrics = {"error": str(e)}
    
    # Copy to frontend
    # /Users/rachelwang/git/ai-partner-catalyst/muse_ai/backend/main.py
    # -> ../../muse_ai/frontend/public/generated_track.mid
    project_root = os.path.dirname(os.path.dirname(script_dir)) 
    # Actually, simplistic: script_dir is muse_ai/backend
    # frontend/public is ../frontend/public
    public_dir = os.path.join(script_dir, "../frontend/public")
    if not os.path.exists(public_dir):
        # Fallback if structure is weird
        public_dir = os.path.join(project_root, "muse_ai/frontend/public")
        
    public_path = os.path.join(public_dir, "generated_track.mid")
    shutil.copy(generated_path, public_path)
    
    return {
        "status": "success",
        "midi_path": "/generated_track.mid",
        "metadata": params,
        "evaluation": eval_metrics
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
