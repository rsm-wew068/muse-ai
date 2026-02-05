"""
Simplified Spotify API test - using search instead of recommendations
"""

from dotenv import load_dotenv
load_dotenv("../.env")

import os
import requests
import base64

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
    
    def search_tracks(self, query, limit=5):
        """Search for tracks"""
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["tracks"]["items"]
    
    def get_audio_features(self, track_ids):
        """Get audio features for multiple tracks"""
        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"ids": ",".join(track_ids)}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["audio_features"]
    
    def print_track_with_features(self, track, features):
        """Pretty print track with audio features"""
        print(f"🎵 {track['name']} - {track['artists'][0]['name']}")
        print(f"   Album: {track['album']['name']}")
        if features:
            print(f"   📊 Valence: {features.get('valence', 0):.2f} | Energy: {features.get('energy', 0):.2f} | Acousticness: {features.get('acousticness', 0):.2f}")
            print(f"   🎹 Tempo: {features.get('tempo', 0):.0f} BPM | Key: {features.get('key', 0)} | Mode: {'Major' if features.get('mode') == 1 else 'Minor'}")
        print(f"   🔗 {track['external_urls']['spotify']}")
        print()

def main():
    tester = SpotifyTester()
    
    # Test 1: Melancholic/Sad vibe
    print("=" * 70)
    print("TEST 1: Melancholic Rainy Day Vibe")
    print("=" * 70)
    print("Query: 'sad indie acoustic melancholic'\n")
    
    tracks = tester.search_tracks("sad indie acoustic melancholic", limit=5)
    track_ids = [t["id"] for t in tracks]
    features_list = tester.get_audio_features(track_ids)
    
    for track, features in zip(tracks, features_list):
        tester.print_track_with_features(track, features)
    
    # Test 2: Energetic/Happy vibe
    print("=" * 70)
    print("TEST 2: Energetic Party Vibe")
    print("=" * 70)
    print("Query: 'dance pop energetic party happy'\n")
    
    tracks = tester.search_tracks("dance pop energetic party happy", limit=5)
    track_ids = [t["id"] for t in tracks]
    features_list = tester.get_audio_features(track_ids)
    
    for track, features in zip(tracks, features_list):
        tester.print_track_with_features(track, features)
    
    # Test 3: Cinematic/Epic vibe
    print("=" * 70)
    print("TEST 3: Cinematic Epic Vibe")
    print("=" * 70)
    print("Query: 'cinematic epic orchestral soundtrack'\n")
    
    tracks = tester.search_tracks("cinematic epic orchestral soundtrack", limit=5)
    track_ids = [t["id"] for t in tracks]
    features_list = tester.get_audio_features(track_ids)
    
    for track, features in zip(tracks, features_list):
        tester.print_track_with_features(track, features)
    
    # Test 4: Analyze audio features distribution
    print("=" * 70)
    print("TEST 4: Audio Features Analysis")
    print("=" * 70)
    print("Comparing vibes across different queries:\n")
    
    queries = [
        ("Sad/Melancholic", "sad melancholic"),
        ("Happy/Upbeat", "happy upbeat"),
        ("Calm/Peaceful", "calm peaceful ambient")
    ]
    
    for label, query in queries:
        tracks = tester.search_tracks(query, limit=3)
        track_ids = [t["id"] for t in tracks]
        features_list = tester.get_audio_features(track_ids)
        
        avg_valence = sum(f.get("valence", 0) for f in features_list if f) / len(features_list)
        avg_energy = sum(f.get("energy", 0) for f in features_list if f) / len(features_list)
        avg_acousticness = sum(f.get("acousticness", 0) for f in features_list if f) / len(features_list)
        
        print(f"{label}:")
        print(f"  Avg Valence: {avg_valence:.2f} (0=sad, 1=happy)")
        print(f"  Avg Energy: {avg_energy:.2f} (0=calm, 1=energetic)")
        print(f"  Avg Acousticness: {avg_acousticness:.2f} (0=electronic, 1=acoustic)")
        print()

if __name__ == "__main__":
    main()
