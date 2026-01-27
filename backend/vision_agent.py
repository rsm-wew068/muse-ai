from dotenv import load_dotenv
load_dotenv("../.env")

import google.generativeai as genai
import os
import json
from PIL import Image
import io

class VisionAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found")
    
    def analyze_image(self, image_data: bytes) -> dict:
        """
        Analyzes an image and extracts musical vibe/mood/genre.
        Returns structured data for Spotify search.
        """
        if not self.model:
            return self._mock_analysis()
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            prompt = """
            Analyze this image and describe the musical vibe it evokes.
            
            Return ONLY valid JSON with these fields:
            {
                "mood": "string (e.g., energetic, melancholic, peaceful, intense)",
                "genre": "string (e.g., electronic, indie, jazz, rock)",
                "tempo": "string (fast, medium, slow)",
                "keywords": ["array", "of", "descriptive", "words"],
                "scene_description": "brief description of what you see and the vibe"
            }
            """
            
            response = self.model.generate_content([prompt, image])
            text = response.text
            
            # Clean JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"Vision analysis error: {e}")
            return self._mock_analysis()
    
    def _mock_analysis(self):
        return {
            "mood": "energetic",
            "genre": "electronic",
            "tempo": "fast",
            "keywords": ["vibrant", "urban", "modern"],
            "scene_description": "Mock analysis - API key not configured"
        }
