from dotenv import load_dotenv
load_dotenv("../.env")

import google.generativeai as genai
import os

class TrackExplainer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found")
    
    def explain_match(self, vibe_analysis: dict, track: dict) -> str:
        """
        Uses Gemini Flash to explain why a track matches the photo's vibe.
        """
        if not self.model:
            return f"This track matches the {vibe_analysis.get('mood', 'vibe')} you're looking for."
        
        prompt = f"""
        Photo vibe: {vibe_analysis.get('scene_description', '')}
        Mood: {vibe_analysis.get('mood', '')}
        Genre preference: {vibe_analysis.get('genre', '')}
        
        Recommended track: "{track['name']}" by {track['artist']}
        
        In 1-2 sentences, explain why this track perfectly captures the vibe of the photo.
        Be specific and creative. Don't use generic phrases.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Explanation error: {e}")
            return f"This {vibe_analysis.get('genre', 'track')} captures the {vibe_analysis.get('mood', 'mood')} energy perfectly."
