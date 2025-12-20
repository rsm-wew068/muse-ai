import os
import glob
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from music21 import converter, note, chord, instrument
import numpy as np
from model import MusicLSTM, SimpleTokenizer
from tqdm import tqdm

# Resolve absolute path to data directory
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data", "midi_dataset", "pop909")
MODEL_PATH = os.path.join(script_dir, "music_lstm.pth")
VOCAB_PATH = os.path.join(script_dir, "vocab.npy")
SEQ_LENGTH = 32
BATCH_SIZE = 64
EPOCHS = 10 # Short training for demo
hidden_size = 256

def parse_midi_files(root_dir, limit=50):
    """
    Parses MIDI files and extracts a sequence of (pitch, duration) strings.
    """
    sequences = []
    # Updated to find files recursively in all subdirectories
    search_path = os.path.join(root_dir, "**", "*.mid")
    files = glob.glob(search_path, recursive=True)
    
    # Filter out files that start with '.' or are in __MACOSX
    files = [f for f in files if "MACOSX" not in f and not os.path.basename(f).startswith('.')]
    
    files = files[:limit] # Limit dataset size for speed
    
    print(f"Parsing {len(files)} MIDI files from {root_dir}...")
    
    for f in tqdm(files):
        try:
            midi = converter.parse(f)
            # Flatten to parts
            try:
                s2 = instrument.partitionByInstrument(midi)
                notes_to_parse = s2.parts[0].recurse() 
            except:
                notes_to_parse = midi.flat.notes
                
            seq = []
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    # Quantize duration to nearest 0.25
                    dur = round(element.duration.quarterLength * 4) / 4
                    seq.append(f"{element.pitch.nameWithOctave}_{dur}")
                elif isinstance(element, chord.Chord):
                    # Take the root note for simplicity
                    dur = round(element.duration.quarterLength * 4) / 4
                    seq.append(f"{element.root().nameWithOctave}_{dur}")
            
            if len(seq) > SEQ_LENGTH:
                sequences.append(seq)
        except Exception as e:
            # print(f"Failed to parse {f}: {e}")
            pass
            
    return sequences

class MusicDataset(Dataset):
    def __init__(self, sequences, tokenizer, seq_length=32):
        self.tokenizer = tokenizer
        self.seq_length = seq_length
        self.data = []
        
        for seq in sequences:
            # Encode
            encoded = tokenizer.encode(seq)
            # Create sliding windows
            for i in range(0, len(encoded) - seq_length, 20): # Stride 20
                self.data.append(encoded[i : i + seq_length + 1])
                
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        chunk = self.data[idx]
        x = torch.tensor(chunk[:-1], dtype=torch.long)
        y = torch.tensor(chunk[1:], dtype=torch.long)
        return x, y

def train():
    # 1. Parse Data
    sequences = parse_midi_files(DATA_DIR, limit=50) # Use 50 songs for quick training
    
    # 2. Build Tokenizer
    tokenizer = SimpleTokenizer()
    all_tokens = set()
    for s in sequences:
        all_tokens.update(s)
    
    for t in all_tokens:
        tokenizer.add_token(t)
    tokenizer.save(VOCAB_PATH)
    print(f"Vocabulary Size: {len(tokenizer.vocab)}")
    
    # 3. Create Dataset
    dataset = MusicDataset(sequences, tokenizer, SEQ_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # 4. Initialize Model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training on {device}")
    
    model = MusicLSTM(len(tokenizer.vocab), hidden_size=hidden_size).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 5. Training Loop
    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        for x, y in pbar:
            x, y = x.to(device), y.to(device)
            
            optimizer.zero_grad()
            output, _ = model(x)
            
            # Reshape for loss
            # output: (batch, seq, vocab), y: (batch, seq)
            loss = criterion(output.view(-1, len(tokenizer.vocab)), y.view(-1))
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            pbar.set_postfix({'loss': loss.item()})
            
        print(f"Epoch {epoch+1} Loss: {total_loss / len(dataloader):.4f}")
        
    # 6. Save Model
    torch.save(model.state_dict(), MODEL_PATH)
    print("Model saved!")

if __name__ == "__main__":
    train()
