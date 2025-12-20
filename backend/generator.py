from music21 import stream, note, chord, tempo, meter, key, scale, pitch, instrument
import random
import torch
import os
import numpy as np
from model import MusicLSTM, SimpleTokenizer

class MusicGenerator:
    def __init__(self):
        self.use_neural = True
        self.model = None
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load Model if available
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "music_lstm.pth")
        vocab_path = os.path.join(script_dir, "vocab.npy")
        
        if os.path.exists(model_path) and os.path.exists(vocab_path):
            try:
                self.tokenizer = SimpleTokenizer()
                self.tokenizer.load(vocab_path)
                
                self.model = MusicLSTM(len(self.tokenizer.vocab)).to(self.device)
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self.model.eval()
                print("Neural Model Loaded Successfully!")
            except Exception as e:
                print(f"Failed to load neural model: {e}")
                self.use_neural = False
        else:
            print("Neural model not found. Falling back to algorithmic.")
            self.use_neural = False

    def generate_music_from_params(self, params: dict, output_path: str = "output.mid"):
        if self.use_neural:
            return self._generate_neural(params, output_path)
        else:
            return self._generate_algorithmic(params, output_path)

    def _generate_neural(self, params: dict, output_path: str):
        print("Generating with Neural Model...")
        s = stream.Score()
        p = stream.Part()
        p.insert(0, instrument.Piano())
        
        # Use params to seed the generation if possible, or just random seed
        # For now, we generate a random sequence.
        # Future: Use 'mood' to select a seed token (e.g., Minor for Sad)
        
        # Seed
        seed = [self.tokenizer.vocab.get("<START>", 0)]
        inp = torch.tensor([seed], dtype=torch.long).to(self.device)
        hidden = None
        
        generated_seq = []
        max_len = 100 # 100 notes
        
        with torch.no_grad():
            for _ in range(max_len):
                out, hidden = self.model(inp, hidden)
                # out: (1, 1, vocab)
                
                # Temperature sampling
                temperature = 0.8
                probs = torch.softmax(out[0, -1] / temperature, dim=0).cpu().numpy()
                
                next_idx = np.random.choice(len(probs), p=probs)
                
                # convert back to token
                token = self.tokenizer.inv_vocab.get(next_idx, "<UNK>")
                
                if token == "<END>":
                    break
                    
                generated_seq.append(token)
                
                # Next input
                inp = torch.tensor([[next_idx]], dtype=torch.long).to(self.device)
        
        # Determine Tempo from params
        bpm = params.get("tempo", 120)
        s.insert(0, tempo.MetronomeMark(number=bpm))
        
        # Convert tokens to Notes
        current_offset = 0.0
        for token in generated_seq:
            if "_" not in token: continue
            
            try:
                pitch_str, dur_val = token.split("_")
                dur_val = float(dur_val)
                
                n = note.Note(pitch_str)
                n.duration.quarterLength = dur_val
                p.insert(current_offset, n)
                
                current_offset += dur_val
            except:
                continue
                
        s.insert(0, p)
        s.write('midi', fp=output_path)
        return output_path

    def _generate_algorithmic(self, params: dict, output_path: str):
        """
        Legacy algorithmic generator as fallback.
        """
        s = stream.Score()
        bpm = params.get("tempo", 120)
        key_str = params.get("key", "C_Major").replace("_", " ")
        mood = params.get("mood", "Neutral")
        
        # ... (Simplified Algorithmic Logic for brevity, usually full implementation here)
        p = stream.Part()
        p.insert(0, instrument.Piano())
        n = note.Note("C4")
        n.duration.quarterLength = 4
        p.insert(0, n)
        s.insert(0, p)
        s.write('midi', fp=output_path)
        return output_path
