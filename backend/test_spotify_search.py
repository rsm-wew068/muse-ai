"""
Test Spotify Search API - This is what we'll actually use in the app
"""

from dotenv import load_dotenv
load_dotenv("../.env")

import os
import requests
import base64

class SpotifySearchTester:
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
    
    def print_tracks(self, tracks, title):
        """Pretty print tracks"""
        print(f"\n{'='*70}")
        print(f"{title}")
        print(f"{'='*70}\n")
        
        for i, track in enumerate(tracks, 1):
            print(f"{i}. 🎵 {track['name']}")
            print(f"   👤 {track['artists'][0]['name']}")
            print(f"   💿 {track['album']['name']}")
            print(f"   🔗 {track['external_urls']['spotify']}")
            if track.get('preview_url'):
                print(f"   🎧 Preview: {track['preview_url']}")
            print()

def main():
    tester = SpotifySearchTester()
    
    # Simulate different photo vibes
    test_cases = [
        {
            "title": "TEST 1: Melancholic Rainy Day (Low Valence, Low Energy)",
            "query": "sad melancholic indie acoustic rain",
            "description": "Photo: Rainy window, gray skies, cozy indoors"
        },
        {
            "title": "TEST 2: Energetic Sunset Party (High Valence, High Energy)",
            "query": "happy energetic dance party upbeat",
            "description": "Photo: Sunset beach party, people dancing"
        },
        {
            "title": "TEST 3: Cinematic Epic Landscape (Medium Valence, Medium Energy)",
            "query": "cinematic epic orchestral majestic grand",
            "description": "Photo: Golden Gate Bridge, grand architecture"
        },
        {
            "title": "TEST 4: Peaceful Morning Coffee (Medium Valence, Low Energy)",
            "query": "calm peaceful morning coffee acoustic chill",
            "description": "Photo: Coffee shop, morning light, relaxed"
        },
        {
            "title": "TEST 5: Urban Night Vibes (Medium Valence, Medium Energy)",
            "query": "urban night city electronic ambient modern",
            "description": "Photo: City lights at night, neon signs"
        }
    ]
    
    for test in test_cases:
        print(f"\n📸 {test['description']}")
        print(f"🔍 Search Query: '{test['query']}'")
        
        tracks = tester.search_tracks(test['query'], limit=5)
        tester.print_tracks(tracks, test['title'])
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY: Spotify Search API Works!")
    print("="*70)
    print("\n✅ We can use keyword-based search for the MVP")
    print("✅ Gemini will translate photo vibes → search keywords")
    print("✅ For v2, we could add audio features filtering (requires user auth)")
    print("\n💡 Next Step: Integrate this into the Musicologist agent")

if __name__ == "__main__":
    main()
