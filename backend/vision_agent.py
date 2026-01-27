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
    
    def analyze_image(self, image_data: bytes, user_feedback: str = None) -> dict:
        """
        Analyzes an image and extracts detailed musical parameters.
        Iteratively refines based on user_feedback if provided.
        """
        if not self.model:
            return self._mock_analysis()
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            base_prompt = """
            You are a master Music Supervisor and Visual Artist. 
            Analyze this image deeply. Look beyond simple objects. 
            What is the story? What is the *implied* temperature, noise level, and emotion?
            
            Translate this visual information into technical Musical Audio Features.

            IMPORTANT: When selecting 'seed_genres', you MUST choose from this list of valid Spotify genres ONLY:
            [acoustic, afrobeat, alt-rock, alternative, ambient, anime, black-metal, bluegrass, blues, bossanova, brazil, breakbeat, british, cantopop, chicago-house, children, chill, classical, club, comedy, country, dance, dancehall, death-metal, deep-house, disco, disney, drum-and-bass, dub, dubstep, edm, electro, electronic, emo, folk, funk, garage, german, gospel, goth, grindcore, groove, grunge, guitar, happy, hard-rock, hardcore, hardstyle, heavy-metal, hip-hop, holidays, house, idm, indian, indie, indie-pop, industrial, iranian, j-dance, j-idol, j-pop, j-rock, jazz, k-pop, kids, latin, latino, malay, mandopop, metal, metal-misc, metalcore, minimal-techno, movies, mpb, new-age, new-release, opera, pagode, party, philippines-opm, piano, pop, pop-film, post-dubstep, power-pop, progressive-house, psych-rock, punk, punk-rock, r-n-b, rainy-day, reggae, reggaeton, road-trip, rock, rock-n-roll, rockabilly, romance, sad, salsa, samba, sertanejo, show-tunes, singer-songwriter, ska, sleep, songwriter, soul, soundtracks, spanish, study, summer, swedish, synth-pop, tango, techno, trance, trip-hop, turkish, work-out, world-music]
            """
            
            json_structure = """
            Return ONLY valid JSON with this exact structure:
            {
                "scene_narrative": "A poetic description of the scene and its underlying story.",
                "mood_keywords": ["list", "of", "5", "adjectives"],
                "musical_parameters": {
                    "seed_genres": ["list", "of", "2", "VALID_GENRES_FROM_LIST"],
                    "target_valence": 0.5,  # (0.0 is sad/depressing, 1.0 is happy/cheerful)
                    "target_energy": 0.5,   # (0.0 is calm, 1.0 is intense/fast)
                    "target_danceability": 0.5, # (0.0 is static, 1.0 is danceable)
                    "target_acousticness": 0.5 # (0.0 is digital, 1.0 is organic/acoustic)
                },
                "search_query_suggestion": "string to use for backup text search"
            }
            """
            
            final_prompt = [base_prompt, json_structure, image]
            
            if user_feedback:
                final_prompt.append(f"\nIMPORTANT UPDATE FROM USER: The user reviewed previous results and said: '{user_feedback}'. adjust your analysis parameters to respect this feedback.")

            response = self.model.generate_content(final_prompt)
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
            "scene_narrative": "A mock description of a city skyline at night (API Key Missing).",
            "mood_keywords": ["urban", "neon", "fast"],
            "musical_parameters": {
                "seed_genres": ["electronic", "synth-pop"],
                "target_valence": 0.7,
                "target_energy": 0.8,
                "target_danceability": 0.9,
                "target_acousticness": 0.1
            },
            "search_query_suggestion": "neon city night drive"
        }
