import torch
import torch.nn as nn
import numpy as np

class MusicLSTM(nn.Module):
    def __init__(self, vocab_size, embed_size=128, hidden_size=256, num_layers=2, dropout=0.3):
        super(MusicLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, x, hidden=None):
        # x shape: (batch_size, seq_length)
        embeds = self.embedding(x)
        # embeds shape: (batch_size, seq_length, embed_size)
        
        out, hidden = self.lstm(embeds, hidden)
        # out shape: (batch_size, seq_length, hidden_size)
        
        # We want the output for the last time step for generation,
        # or all time steps for training.
        out = self.fc(out)
        # out shape: (batch_size, seq_length, vocab_size)
        return out, hidden

class SimpleTokenizer:
    """
    A simple tokenizer that maps (pitch, duration) tuples to integers.
    """
    def __init__(self):
        self.vocab = {}
        self.inv_vocab = {}
        self.counter = 0
        
        # Special tokens
        self.add_token("<PAD>")
        self.add_token("<START>")
        self.add_token("<END>")
    
    def add_token(self, token):
        if token not in self.vocab:
            self.vocab[token] = self.counter
            self.inv_vocab[self.counter] = token
            self.counter += 1
            
    def encode(self, sequence):
        return [self.vocab.get(t, 0) for t in sequence]
        
    def decode(self, indices):
        return [self.inv_vocab.get(i, "<UNK>") for i in indices]
        
    def save(self, path):
        np.save(path, self.vocab)
        
    def load(self, path):
        self.vocab = np.load(path, allow_pickle=True).item()
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.counter = len(self.vocab)
