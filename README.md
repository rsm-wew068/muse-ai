# Muse.AI 🎵
> *The Agentic DJ that sees, listens, and reasons.*

**Muse.AI** is a multimodal AI agent that analyzes the narrative of your photos to curate a deeply personalized soundtrack. Unlike simple keyword swappers, Muse.AI uses a **LangGraph-based reasoning engine** to understand the *story* behind an image, translate it into psycho-acoustic parameters, and critique its own choices before presenting them to you.

## 🧠 The "Muse" Agent Architecture

Muse.AI isn't just a script; it's a stateful graph of specialized agents working together:

1.  **👁️ The Visionary (Gemini 3 Flash - Multimodal)**:
    *   Looks beyond objects. Analyzes lighting, texture, and implied narrative (e.g., "solitude at 3 AM").
    *   Extracts a poetic "Scene Narrative" and specific audio targets (Valence, Energy, Acousticness).
2.  **🎼 The Musicologist (Algorithm)**:
    *   Translates emotions into Spotify's technical `audio_features`.
    *   Selects valid genre seeds based on the visual aesthetic.
3.  **⚖️ The Critic (Gemini 3 Flash)**:
    *   Reviews the candidate tracks found by Spotify.
    *   *"Does this Death Metal song fit a Sleeping Baby photo?"* -> **Rejects bad matches.**
4.  **🗣️ The Feedback Loop (Human-in-the-Loop)**:
    *   Users can chat with the agent ("Make it more 80s") to refine the playlist in real-time.

## 🚀 Key Features
*   **Deep Multimodal Reasoning**: Connects visual pixel data to abstract musical theory.
*   **Iterative Refinement**: The agent holds state, allowing for conversational adjustments.
*   **Technical Precision**: Visualizes the exact 'Valence' and 'Energy' detected in your photo.
*   **Production Ready**: Containerized and deployed on Google Cloud Run.

## 🛠️ Tech Stack

### AI & Agent Framework
*   **Google Gemini 3 Flash**: Used for both Multimodal Vision analysis and Text generation/reasoning.
*   **LangGraph**: Stateful agent orchestration.
*   **LangChain**: Model tooling.

### Application
*   **Frontend**: Next.js 16 (React 19) + TailwindCSS v4 + Glassmorphism UI.
*   **Backend**: FastAPI (Python) + Pydantic.
*   **Infrastructure**: Docker + Google Cloud Run.

## ⚡️ Quick Start

### Prerequisites
*   Python 3.11+
*   Node.js 18+
*   Google Gemini API Key
*   Spotify API Credentials

### 1. Backend Setup
```bash
cd backend

# Install dependencies including LangGraph
pip install -r requirements.txt

# Set up Environment Variables
# Create .env file in project root with:
GEMINI_API_KEY=your_gemini_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Run the Agent API
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

## ☁️ Deployment (Google Cloud Run)

We have included a one-click deployment script for GCP.

1.  Ensure you have the `gcloud` CLI installed and authenticated.
2.  Run the script:
    ```bash
    ./deploy_gcp.sh
    ```
3.  This will:
    *   Build Docker images for Frontend & Backend.
    *   Push them to Google Artifact Registry.
    *   Deploy them to Cloud Run as auto-scaling services.

## 🧠 System Architecture Diagram

`[User Image]` -> **Vision Agent** -> `(Narrative + Audio Params)` -> **Spotify Tool** -> `(Raw Candidates)` -> **Critic Agent** -> `(Curated Playlist)` -> **User UI**

---
*Built for the Gemini 3 Global Hackathon*
