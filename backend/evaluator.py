import google.generativeai as genai
import os
import json
from state import Track, Recommendation

class Evaluator:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None

    def evaluate_tracks(self, scene_narrative: str, tracks: list[Track]) -> list[Recommendation]:
        """
        Critiques tracks against the scene narrative.
        Returns curated list of recommendations with explanations.
        """
        if not self.model:
            return self._mock_eval(tracks)
            
        try:
            prompt = f"""
            You are a strict Music Critic and Curator.
            
            SCENE NARRATIVE:
            "{scene_narrative}"
            
            CANDIDATE TRACKS (Total: {len(tracks)}):
            {json.dumps([{ 'id': t['id'], 'name': t['name'], 'artist': t['artist'] } for t in tracks])}
            
            TASK:
            1. Analyze all {len(tracks)} candidates.
            2. FILTER: Discard generic matches. Keep only tracks that deeply resonate with the scene's mood.
            3. RERANK: Select top 5 tracks.
            4. EXPLAIN: Write a creative 1-sentence explanation for each.
            
            Return ONLY valid JSON:
            {{
                "recommendations": [
                    {{
                        "track_id": "id_from_input",
                        "match_score": 95,
                        "explanation": "Why this song fits..."
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Clean JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            result = json.loads(text.strip())
            
            # Merit candidates back to full objects
            final_recs = []
            for rec in result.get("recommendations", []):
                # Find original track object
                original = next((t for t in tracks if t["id"] == rec["track_id"]), None)
                if original:
                    final_recs.append({
                        "track": original,
                        "explanation": rec.get("explanation", "Matches the vibe."),
                        "match_score": rec.get("match_score", 80),
                        "match_reason": "AI Curation"
                    })
            
            return final_recs
        except Exception as e:
            print(f"Evaluator error: {e}")
            return self._mock_eval(tracks)

    def _mock_eval(self, tracks):
        return [{
            "track": t,
            "explanation": "Mock explanation - AI offline.",
            "match_score": 85,
            "match_reason": "Mock"
        } for t in tracks[:5]]
