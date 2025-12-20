from dotenv import load_dotenv
load_dotenv("../../.env") # Load from project root

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("Warning: google-generativeai not installed.")

import os
import json

class MusicAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        else:
            self.model = None

    def _get_deterministic_mock(self, user_prompt, feedback_history=[]):
        print(f"Using Deterministic Mock for prompt: '{user_prompt}'")
        import hashlib
        
        # Keyword overrides for better demo experience offline
        p_lower = user_prompt.lower()
        
        # Check for negative feedback to "pivot"
        downvotes = len([f for f in feedback_history if f['rating'] == 'down'])
        pivot_offset = downvotes * 762 # Arbitrary prime to shift hash significantly
        
        # If we have downvotes, we skip the simple cache and go chaotic (random/hashed)
        # unless it's the first time
        
        if downvotes == 0:
            if "rock" in p_lower or "energetic" in p_lower or "fast" in p_lower:
                return {"tempo": 140, "key": "E_Major", "tokens": [], "mood": "Energetic"}
            if "sad" in p_lower or "slow" in p_lower or "dark" in p_lower:
                 return {"tempo": 70, "key": "C_Minor", "tokens": [], "mood": "Sad"}
            if "happy" in p_lower or "pop" in p_lower:
                 return {"tempo": 120, "key": "C_Major", "tokens": [], "mood": "Happy"}
             
        # Hash the prompt to get stable numbers for other inputs (plus pivot)
        h = int(hashlib.sha256(user_prompt.encode()).hexdigest(), 16) + pivot_offset
        
        # Deterministic Tempo (60 - 180)
        tempos = [80, 100, 120, 140, 160]
        tempo = tempos[h % len(tempos)]
        
        # Deterministic Key
        keys = ["C_Major", "C_Minor", "F_Major", "F_Minor", "G_Major", "D_Minor"]
        key = keys[(h // 10) % len(keys)]
        
        # Deterministic Mood
        moods = ["Happy", "Sad", "Energetic", "Chill", "Dark"]
        mood = moods[(h // 100) % len(moods)]
        
        return {
            "tempo": tempo,
            "key": key,
            "tokens": [],
            "mood": mood
        }

    def analyze_intent(self, user_prompt, feedback_history=[]):
        """
        Converts user natural language to musical parameters.
        Includes RLHF context.
        """
        if not self.model:
            print(f"Gemini not configured (Key present: {bool(self.api_key)}).")
            return self._get_deterministic_mock(user_prompt, feedback_history)
            
        system_prompt = f"""
        You are a Music Producer. Convert the user's description into technical parameters.
        Return strictly valid JSON.
        
        Context: The user has provided feedback on previous attempts: {feedback_history}.
        If the user voted 'down', you MUST change the interpretation significantly (e.g. swap major/minor, change tempo).
        
        Fields:
        - tempo (int)
        - key (str, e.g. "C_Minor")
        - mood (str)
        - seed_tokens (list of str, e.g. ["Track_Melody", "Note_C4"]): detailed tokens for the start of the song.
        """
        
        try:
            response = self.model.generate_content(f"{system_prompt}\nUser: {user_prompt}")
            text = response.text
            # Clean up json markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            # Use deterministic mock as fallback instead of static error
            return self._get_deterministic_mock(user_prompt)
