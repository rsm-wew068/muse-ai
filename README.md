# Muse.AI 🎵
> *The Artificial Composer Studio: Where Neuro-Symbolic AI meets Creative Expression.*

**Muse.AI** is an intelligent music generation platform that translates natural language descriptions into original symbolic music compositions. By bridging Large Language Models (Gemini) with deep learning sequence models (LSTM), it allows users to generate, visualize, and refine music through a conversational interface.

## 🚀 Key Features

*   **Natural Language Conductor**: Describe your vibe (e.g., *"Cyberpunk chase in the rain"*) and let our **Gemini-powered Agent** translate abstract concepts into technical musical parameters (Key, Tempo, Mood).
*   **Neuro-Symbolic Generation**: Combines the reasoning power of LLMs with a custom-trained **PyTorch LSTM** model to generate melodically consistent MIDI sequences.
*   **Active Learning Loop (RLHF)**: Interactive "Thumbs Up/Down" feedback mechanism that fine-tunes future generations based on your preferences.
*   **Real-time Visualization**: Browser-based MIDI rendering and audio playback using **Magenta.js**.

## 🛠️ Tech Stack

### Frontend
*   **Framework**: [Next.js 16](https://nextjs.org/) (React 19)
*   **Styling**: TailwindCSS v4 with Glassmorphism UI
*   **Audio Engine**: @magenta/music (SoundFonts & Visualization)

### Backend
*   **API**: FastAPI
*   **AI Agent**: Google Gemini Pro (via `google-generativeai`)
*   **Core Model**: PyTorch (LSTM trained on POP909 dataset)
*   **Music Processing**: Music21

## ⚡️ Quick Start

### Prerequisites
*   Python 3.9+
*   Node.js 18+
*   Google Gemini API Key

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Environment
# Create a .env file in the root or export the variable directly
export GEMINI_API_KEY="your_api_key_here"

# Run the Orchestrator
python main.py
```
*Server runs on `http://localhost:8000`*

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```
*App runs on `http://localhost:3000`*

## 🧠 System Architecture

1.  **Intent Analysis (Gemini)**: User prompt is analyzed to extract musical constraints (e.g., "Sad" -> Minor Key, Slow Tempo).
2.  **Parameter Injection**: These constraints seed the **Music Generator**.
3.  **Sequence Generation (LSTM)**: The neural network predicts note-by-note sequences based on the seed.
4.  **Rendering**: The resulting MIDI is sent to the frontend for synthesis and visualization.
