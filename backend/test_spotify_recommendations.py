"""
Test script for Spotify Recommendations API
Tests audio features-based recommendations (valence, energy, acousticness, etc.)
"""

from dotenv import load_dotenv
load_dotenv("../.env")

import os
import requests
import base64
import json

class SpotifyTester:
    def __init__(self):
        self.client_id = os.environ.get("SPOTIFY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
        self.access_token = None
        self._authenticate()
    
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
        
        response = requests.post(auth_url, headers=headers, data=data)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        print("✅ Authenticated with Spotify\n")
    
    def search_seed_tracks(self, query, limit=1):
        """Search for seed tracks to use in recommendations"""
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        tracks = response.json()["tracks"]["items"]
        return [t["id"] for t in tracks]
    
    def get_recommendations(self, seed_tracks=None, seed_artists=None, seed_genres=None,
                           target_valence=None, target_energy=None, 
                           target_acousticness=None, target_tempo=None, limit=10):
        """
        Get recommendations based on audio features
        
        Note: Need at least 1 seed (track, artist, or genre). Max 5 seeds total.
        
        Audio Features:
        - valence: 0.0 (sad) to 1.0 (happy)
        - energy: 0.0 (calm) to 1.0 (energetic)
        - acousticness: 0.0 (electronic) to 1.0 (acoustic)
        - tempo: BPM (e.g., 120)
        """
        url = "https://api.spotify.com/v1/recommendations"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        params = {"limit": limit}
        
        # Need at least one seed
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:5])
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:5])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:5])
        
        if target_valence is not None:
            params["target_valence"] = target_valence
        
        if target_energy is not None:
            params["target_energy"] = target_energy
        
        if target_acousticness is not None:
            params["target_acousticness"] = target_acousticness
        
        if target_tempo is not None:
            params["target_tempo"] = target_tempo
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
        response.raise_for_status()
        return response.json()
    
    def get_available_genres(self):
        """Get list of available seed genres"""
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["genres"]
        except:
            # Fallback to common genres if API fails
            return ["ambient", "indie", "dance", "pop", "classical", "soundtrack", 
                    "jazz", "rock", "electronic", "hip-hop", "r-n-b", "country"]
    
    def print_tracks(self, tracks):
        """Pretty print track list"""
        for i, track in enumerate(tracks, 1):
            print(f"{i}. {track['name']} - {track['artists'][0]['name']}")
            print(f"   Album: {track['album']['name']}")
            print(f"   Spotify: {track['external_urls']['spotify']}")
            print()

def main():
    tester = SpotifyTester()
    
    # Test 1: Get available genres
    print("=" * 60)
    print("TEST 1: Available Genre Seeds")
    print("=" * 60)
    genres = tester.get_available_genres()
    print(f"Found {len(genres)} genres")
    print(f"Sample genres: {', '.join(genres[:10])}")
    print()
    
    # Test 2: Melancholic/Sad vibe (like rainy day photo)
    print("=" * 60)
    print("TEST 2: Melancholic Rainy Day Vibe")
    print("=" * 60)
    print("Getting seed track for 'sad indie'...")
    seed_tracks = tester.search_seed_tracks("sad indie acoustic")
    print(f"Seed track ID: {seed_tracks[0] if seed_tracks else 'None'}")
    print()
    print("Parameters:")
    print("  - Valence: 0.2 (sad)")
    print("  - Energy: 0.3 (low)")
    print("  - Acousticness: 0.7 (acoustic)")
    print()
    
    result = tester.get_recommendations(
        seed_tracks=seed_tracks,
        target_valence=0.2,
        target_energy=0.3,
        target_acousticness=0.7,
        limit=5
    )
    tester.print_tracks(result["tracks"])
    
    # Test 3: Energetic/Happy vibe (like sunset party photo)
    print("=" * 60)
    print("TEST 3: Energetic Sunset Party Vibe")
    print("=" * 60)
    print("Getting seed track for 'dance pop'...")
    seed_tracks = tester.search_seed_tracks("dance pop party")
    print(f"Seed track ID: {seed_tracks[0] if seed_tracks else 'None'}")
    print()
    print("Parameters:")
    print("  - Valence: 0.8 (happy)")
    print("  - Energy: 0.9 (high)")
    print("  - Tempo: 128 BPM")
    print()
    
    result = tester.get_recommendations(
        seed_tracks=seed_tracks,
        target_valence=0.8,
        target_energy=0.9,
        target_tempo=128,
        limit=5
    )
    tester.print_tracks(result["tracks"])
    
    # Test 4: Cinematic/Epic vibe (like Golden Gate Bridge photo)
    print("=" * 60)
    print("TEST 4: Cinematic Epic Vibe")
    print("=" * 60)
    print("Getting seed track for 'cinematic epic'...")
    seed_tracks = tester.search_seed_tracks("cinematic epic orchestral")
    print(f"Seed track ID: {seed_tracks[0] if seed_tracks else 'None'}")
    print()
    print("Parameters:")
    print("  - Valence: 0.5 (neutral)")
    print("  - Energy: 0.6 (moderate)")
    print("  - Acousticness: 0.4 (orchestral)")
    print()
    
    result = tester.get_recommendations(
        seed_tracks=seed_tracks,
        target_valence=0.5,
        target_energy=0.6,
        target_acousticness=0.4,
        limit=5
    )
    tester.print_tracks(result["tracks"])
    
    # Test 5: Get audio features for a track
    print("=" * 60)
    print("TEST 5: Audio Features Analysis")
    print("=" * 60)
    print("Getting audio features for first recommended track...")
    print()
    
    if result["tracks"]:
        track_id = result["tracks"][0]["id"]
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = {"Authorization": f"Bearer {tester.access_token}"}
        
        response = requests.get(url, headers=headers)
        features = response.json()
        
        print(f"Track: {result['tracks'][0]['name']}")
        print(f"Valence: {features.get('valence', 'N/A'):.2f}")
        print(f"Energy: {features.get('energy', 'N/A'):.2f}")
        print(f"Acousticness: {features.get('acousticness', 'N/A'):.2f}")
        print(f"Danceability: {features.get('danceability', 'N/A'):.2f}")
        print(f"Tempo: {features.get('tempo', 'N/A'):.1f} BPM")
        print(f"Key: {features.get('key', 'N/A')}")
        print(f"Mode: {'Major' if features.get('mode') == 1 else 'Minor'}")

if __name__ == "__main__":
    main()
