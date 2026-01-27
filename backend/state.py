from typing import List, Dict, TypedDict, Optional, Any

class Track(TypedDict):
    id: str
    name: str
    artist: str
    album_art: Optional[str]
    preview_url: Optional[str]
    external_url: str

class Recommendation(TypedDict):
    track: Track
    explanation: str
    match_score: int
    match_reason: str

class MuseState(TypedDict):
    image_data: bytes
    vibe_description: str
    search_parameters: Dict[str, Any]
    candidate_tracks: List[Track] 
    final_recommendations: List[Recommendation]
    user_feedback: Optional[str]
    iteration_count: int
