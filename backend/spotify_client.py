from dotenv import load_dotenv
load_dotenv("../.env")

import os
import requests
import base64
import time

class SpotifyClient:
    def __init__(self):
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.access_token = None
        self.token_expires_at = 0
        
        if self.client_id and self.client_secret:
            self._authenticate()
        else:
            print("Warning: Spotify credentials not found")
    
    def _authenticate(self):
        """Get Spotify access token"""
        auth_url = "https://accounts.spotify.com/api/token"
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(auth_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            # Token expires in 3600 seconds, refresh 5 minutes early
            self.token_expires_at = time.time() + token_data.get("expires_in", 3600) - 300
            print("Spotify authenticated successfully")
        except Exception as e:
            print(f"Spotify auth error: {e}")
    
    def _ensure_valid_token(self):
        """Refresh token if expired"""
        if time.time() >= self.token_expires_at:
            print("Token expired, refreshing...")
            self._authenticate()
    
    def get_recommendations(self, seed_genres: list, target_params: dict, limit: int = 10):
        """
        Get recommendations based on audio features (valence, energy, etc.)
        """
        if not self.access_token:
            return self._mock_tracks()
            
        self._ensure_valid_token()
        
        url = "https://api.spotify.com/v1/recommendations"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Valid seeds are required. For now, we trust Gemini or should filter against available seeds.
        # Ideally, we should fetch available seeds and filter.
        
        params = {
            "limit": limit,
            "seed_genres": ",".join(seed_genres[:5]), # Max 5 seeds
            **target_params
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            tracks = response.json()["tracks"]
            
            return [{
                "id": t["id"],
                "name": t["name"],
                "artist": t["artists"][0]["name"],
                "album": t["album"]["name"],
                "preview_url": t.get("preview_url"),
                "spotify_url": t["external_urls"]["spotify"],
                "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
                "duration_ms": t["duration_ms"]
            } for t in tracks]
            
        except requests.exceptions.HTTPError as e:
            print(f"Spotify recommendation error: {e}")
            # Fallback to search if recommendations fail (e.g., invalid seeds)
            return self.search_tracks({"keywords": seed_genres}, limit)
        except Exception as e:
            print(f"Spotify recommendation error: {e}")
            return self._mock_tracks()

    def search_tracks(self, vibe_analysis: dict, limit: int = 5):
        """
        Search Spotify based on vibe analysis (Fallback method).
        Returns list of track objects.
        """
        if not self.access_token:
            return self._mock_tracks()
        
        # Ensure token is valid
        self._ensure_valid_token()
        
        # Build search query from vibe
        # handle legacy or new vibe_analysis structure
        if "musical_parameters" in vibe_analysis:
            # New structure fallback
            keywords = vibe_analysis.get("search_query_suggestion", "")
        else:
            mood = vibe_analysis.get("mood", "")
            genre = vibe_analysis.get("genre", "")
            keywords = " ".join(vibe_analysis.get("keywords", [])[:3])
            keywords = f"{mood} {genre} {keywords}"
        
        query = keywords.strip()
        
        search_url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            tracks = response.json()["tracks"]["items"]
            
            # Simplify track data
            return [{
                "id": t["id"],
                "name": t["name"],
                "artist": t["artists"][0]["name"],
                "album": t["album"]["name"],
                "preview_url": t.get("preview_url"),
                "spotify_url": t["external_urls"]["spotify"],
                "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
                "duration_ms": t["duration_ms"]
            } for t in tracks]
            
        except Exception as e:
            print(f"Spotify search error: {e}")
            return self._mock_tracks()
    
    def _mock_tracks(self):
        return [{
            "id": "mock_id",
            "name": "Mock Track",
            "artist": "Mock Artist",
            "album": "Mock Album",
            "preview_url": None,
            "spotify_url": "https://spotify.com",
            "image": None,
            "duration_ms": 180000
        }]
