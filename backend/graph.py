from langgraph.graph import StateGraph, END
from state import MuseState
from vision_agent import VisionAgent
from spotify_client import SpotifyClient
from evaluator import Evaluator

# Initialize Agents
vision = VisionAgent()
spotify = SpotifyClient()
critic = Evaluator()

# --- Node Definitions ---

def vision_node(state: MuseState):
    """
    Node A: The Visionary (and Listener for feedback).
    Analyzes image OR re-analyzes based on feedback.
    """
    image_data = state["image_data"]
    feedback = state.get("user_feedback")
    
    print(f"--- Vision Node -- Feedback: {feedback}")
    
    analysis = vision.analyze_image(image_data, user_feedback=feedback)
    
    return {
        "vibe_description": analysis.get("scene_narrative", ""),
        "search_parameters": analysis.get("musical_parameters", {}),
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def search_node(state: MuseState):
    """
    Node B: The Scout.
    Fetches raw candidates from Spotify.
    """
    print("--- Search Node ---")
    params = state["search_parameters"]
    seeds = params.get("seed_genres", [])
    
    # Extract audio features
    targets = {
        "target_valence": params.get("target_valence"),
        "target_energy": params.get("target_energy"),
        "target_danceability": params.get("target_danceability"),
        "target_acousticness": params.get("target_acousticness")
    }
    # Clean None values
    targets = {k: v for k, v in targets.items() if v is not None}
    
    if seeds:
        print(f"Searching with seeds: {seeds} and targets: {targets}")
        tracks = spotify.get_recommendations(seeds, targets, limit=15)
    else:
        print("No seeds found, falling back to keyword search")
        # Fallback if Vision params are missing (e.g. mock mode)
        tracks = spotify.search_tracks({"keywords": ["pop"]}, limit=15)
        
    return {"candidate_tracks": tracks}

def curator_node(state: MuseState):
    """
    Node C: The Critical Curator.
    Filters and Explains based on narrative match.
    """
    print("--- Curator Node ---")
    narrative = state.get("vibe_description", "A photo")
    candidates = state.get("candidate_tracks", [])
    
    recommendations = critic.evaluate_tracks(narrative, candidates)
    
    return {"final_recommendations": recommendations}

# --- Graph Construction ---

workflow = StateGraph(MuseState)

workflow.add_node("vision", vision_node)
workflow.add_node("search", search_node)
workflow.add_node("curator", curator_node)

# Linear flow (for now)
# Vision -> Search -> Curator -> End
workflow.set_entry_point("vision")
workflow.add_edge("vision", "search")
workflow.add_edge("search", "curator")
workflow.add_edge("curator", END)

# Compile the graph
muse_graph = workflow.compile()
