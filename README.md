# Muse.AI 🎵
> *Soundtrack for Life: The Multimodal Reasoner with Memory*

**Muse.AI** transforms photos into personalized soundtracks using a multi-agent AI system that **sees, reasons, critiques, and remembers**. Unlike simple keyword matchers, Muse.AI employs specialized agents that understand visual narratives, validate their own recommendations, and learn your taste over time through reinforcement learning.

## 🧠 The "Muse" Agent Architecture

Muse.AI uses a **LangGraph-based state machine** with specialized agents that work together, validate each other, and learn from your feedback:

### The Agent Pipeline

1.  **👁️ The Visionary (Gemini 3 Flash - Multimodal)**
    *   **What it does**: Analyzes photos beyond objects—captures lighting, mood, texture, and implied narrative
    *   **Output**: Poetic "Scene Narrative" (e.g., "solitude at 3 AM, neon-lit streets") + precise audio targets
    *   **Audio Parameters**: Valence (happiness), Energy (intensity), Acousticness, Danceability
    *   **Memory Integration**: Reads your liked tracks history and subtly biases towards your preferred genres *while still respecting the visual context*
    *   **Feedback Aware**: "Make it more upbeat" → recalibrates valence/energy parameters

2.  **🎼 The Musicologist (Hybrid Search)**
    *   **Spotify Recommendations API**: Uses audio features (valence, energy, tempo) for technical matching
    *   **Valid Genre Seeds**: Gemini selects from 150+ valid Spotify genres (no API errors!)
    *   **Precision Targeting**: Maps visual vibes to psycho-acoustic parameters
    *   **Output**: 15 candidate tracks that technically match the scene

3.  **⚖️ The Curator (Gemini 3 Flash - The Critic)**
    *   **What it does**: Acts as quality control—reviews candidates against the scene narrative
    *   **Filters Hallucinations**: *"Does Death Metal fit a Sleeping Baby photo?"* → **Rejected**
    *   **Prevents Mismatches**: Catches when Spotify returns technically correct but contextually wrong tracks
    *   **Explains Reasoning**: Generates creative 1-sentence explanations for each recommendation
    *   **Output**: Top 5 tracks with match scores and explanations

4.  **🧠 Long-Term Memory (Reinforcement Learning Lite)**
    *   **Learns Your Taste**: Every "Like" builds your musical profile
    *   **Persistent Preferences**: Stored in `user_likes.json` across sessions
    *   **Adaptive Recommendations**: Future analyses incorporate your preferred artists and genres
    *   **Context-Aware**: Balances your taste with the photo's vibe (doesn't force jazz onto a metal scene)
    *   **Feedback Loop**: "Make it more 80s" → Re-runs pipeline with adjusted parameters

5.  **🗣️ The Interaction Loop (Human-in-the-Loop)**
    *   **Conversational Refinement**: Refine results without re-uploading photos
    *   **Session Persistence**: Remembers context across interactions
    *   **Iterative Improvement**: Each refinement makes recommendations more precise

## 🚀 Key Features

### 🎨 Visuals to Vibes
*   **Photo Analysis**: Upload any image—sunset, city street, cozy cafe, adventure scene
*   **Scene Understanding**: AI extracts mood, energy, aesthetic, and narrative
*   **Audio Feature Mapping**: Translates visual vibes into Spotify's psycho-acoustic parameters
*   **Beyond Keywords**: Understands implied temperature, noise level, and emotional subtext

### 🧠 Long-Term Memory (Reinforcement Learning Lite)
*   **Learns Your Taste**: Every "Like" trains the system on your preferences
*   **Persistent Profile**: Your musical identity stored across sessions
*   **Adaptive Recommendations**: Future analyses incorporate your preferred artists and genres
*   **Context-Aware Learning**: Balances your taste with the photo's vibe (won't force jazz onto a metal scene)
*   **Feedback Integration**: "Make it more energetic" → System adjusts and remembers

### ⚖️ The Critic (Quality Control)
*   **Filters Hallucinations**: Catches when AI recommends contextually wrong tracks
*   **Validates Matches**: *"Happy Pop for a Funeral?"* → **Rejected**
*   **Prevents Spotify Mismatches**: Technical correctness ≠ contextual fit
*   **Explainable AI**: Every recommendation comes with reasoning
*   **Match Scoring**: Ranks tracks by narrative alignment (0-100)

### 🤖 Agentic Reasoning
*   **Multi-Agent Validation**: Each agent critiques the previous step
*   **Stateful Conversations**: Refine results without re-uploading photos
*   **Iterative Refinement**: "Too slow" → Agent adjusts energy parameters and re-searches
*   **LangGraph Orchestration**: Complex workflows with loops and conditionals

### 🎯 Production Features
*   **Session Management**: Persistent user profiles and preferences
*   **Real-time Stats**: Track your top artists, genres, and listening patterns (coming soon)
*   **Cloud Deployment**: Containerized and ready for Google Cloud Run
*   **API-First Design**: RESTful endpoints for integration

## 🛠️ Tech Stack

### AI & Agent Framework
*   **Google Gemini 3 Flash Preview**: Multimodal vision analysis + text generation/reasoning
*   **LangGraph**: Stateful agent orchestration and workflow management
*   **Vectra**: Local vector database for semantic search over liked tracks
*   **Spotify Web API**: Recommendations API with audio features + track search

### Application Stack
*   **Frontend**: Next.js 16 (React 19) + TailwindCSS v4 + Glassmorphism UI
*   **Backend**: FastAPI (Python 3.11+) + Pydantic for type safety
*   **Storage**: JSON-based persistence + vector embeddings
*   **Infrastructure**: Docker + Google Cloud Run with auto-scaling

### Key Libraries
*   `langgraph` - Agent state machine
*   `google-generativeai` - Gemini API client
*   `spotify-web-api-node` - Spotify integration
*   `vectra` - Vector similarity search
*   `pillow` - Image processing

## ⚡️ Quick Start

### Prerequisites
*   Python 3.11+
*   Node.js 18+
*   Google Gemini API Key ([Get one here](https://ai.google.dev/))
*   Spotify API Credentials ([Create app here](https://developer.spotify.com/dashboard))

### 1. Environment Setup

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies (includes LangGraph, Vectra, FastAPI)
pip install -r requirements.txt

# Run the Agent API
python main.py
```

*Backend runs on `http://localhost:8000`*

**API Endpoints:**
- `POST /analyze-photo` - Upload photo, get recommendations
- `POST /refine` - Provide feedback to refine results
- `POST /like-track` - Save track to your playlists
- `GET /playlists/{user_id}` - Get your saved playlists
- `GET /dashboard/{user_id}` - Get listening stats

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```

*Frontend runs on `http://localhost:3000`*

### 4. First Run

1. Open `http://localhost:3000`
2. Upload a photo (any image that evokes a mood)
3. Wait for the agents to analyze and recommend tracks
4. Like tracks you enjoy to build your profile
5. Try refining: "Make it more energetic" or "Add some jazz"
6. Check the Playlists tab to see your saved tracks
7. View Dashboard for personalized stats

## ☁️ Deployment (Google Cloud Run)

Deploy both frontend and backend as auto-scaling serverless containers:

### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed locally

### One-Click Deployment

```bash
# Make the script executable
chmod +x deploy_gcp.sh

# Deploy (creates Artifact Registry, builds images, deploys to Cloud Run)
./deploy_gcp.sh
```

The script will:
1. Create a Google Artifact Registry repository
2. Build Docker images for frontend and backend
3. Push images to Artifact Registry
4. Deploy to Cloud Run with environment variables
5. Output the public URLs for both services

### Manual Deployment

```bash
# Set your GCP project
export PROJECT_ID=your-gcp-project-id
export REGION=us-central1

# Build and push backend
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/muse-ai-backend
gcloud run deploy muse-ai-backend \
  --image gcr.io/$PROJECT_ID/muse-ai-backend \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET

# Build and push frontend
cd ../frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/muse-ai-frontend
gcloud run deploy muse-ai-frontend \
  --image gcr.io/$PROJECT_ID/muse-ai-frontend \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
```

### Environment Variables for Production

Set these in Cloud Run console or via `gcloud`:
- `GEMINI_API_KEY` - Your Gemini API key
- `SPOTIFY_CLIENT_ID` - Spotify app client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify app secret
- `DATA_DIR` - `/data` (for persistent storage with Cloud Storage mount)

## 🧠 System Architecture

### Data Flow

```
User uploads photo
    ↓
FastAPI creates session + loads user preferences
    ↓
LangGraph State Machine invokes:
    ┌─────────────────────────────────────────┐
    │ 1. VISION NODE (Gemini 3 Flash)        │
    │    - Analyzes image (multimodal)        │
    │    - Reads user's liked tracks history  │
    │    - Extracts scene narrative           │
    │    - Generates audio parameters         │
    │    - Biases towards user's genres       │
    │    - Output: vibe_description + params  │
    └─────────────────────────────────────────┘
                    ↓
    ┌─────────────────────────────────────────┐
    │ 2. SEARCH NODE (Spotify Recommendations)│
    │    - Uses audio features (valence,      │
    │      energy, acousticness, etc.)        │
    │    - Selects valid genre seeds          │
    │    - Queries Spotify Recommendations API│
    │    - Output: 15 candidate tracks        │
    └─────────────────────────────────────────┘
                    ↓
    ┌─────────────────────────────────────────┐
    │ 3. CURATOR NODE (Gemini 3 Flash)        │
    │    - Reviews candidates vs narrative    │
    │    - Filters contextual mismatches      │
    │    - Prevents hallucinations            │
    │    - Scores by narrative alignment      │
    │    - Generates explanations             │
    │    - Output: Top 5 with reasoning       │
    └─────────────────────────────────────────┘
    ↓
Returns: recommendations + session_id
    ↓
User clicks "Like" on track → Stored in:
    - Google Cloud Firestore (Serverless NoSQL)
    - Builds user preference profile
    ↓
(Optional) User sends feedback: "Make it more upbeat"
    ↓
Graph re-runs with:
    - Updated user preferences (includes new likes)
    - Feedback context ("more upbeat")
    - Same photo (from session)
```

### State Object

```python
class MuseState(TypedDict):
    image_data: bytes                    # Original photo
    vibe_description: str                # "Melancholic rainy day..."
    search_parameters: dict              # {valence: 0.2, energy: 0.3, seed_genres: [...]}
    candidate_tracks: list               # Raw results from Spotify
    final_recommendations: list          # Curated top 5 with explanations
    user_feedback: Optional[str]         # "Make it more upbeat"
    user_preferences: Optional[str]      # "User likes: Radiohead, Bon Iver..."
    iteration_count: int                 # Refinement iterations
```

### Personalization Engine

**How Memory Works:**
1. User likes a track → Saved to Firestore
2. On next photo upload → System loads liked tracks
3. Summarizes preferences: "User likes artists: Radiohead, Bon Iver. Recently liked: Fake Plastic Trees, Holocene"
4. Vision Agent receives preferences as context
5. Gemini subtly biases genre selection towards user's taste *while respecting the photo*

**Example:**
```
Photo: Rainy city street at night
User History: Likes indie, folk, acoustic tracks

Without Memory:
→ Genres: electronic, synth-pop
→ Tracks: Kavinsky, M83, The Midnight

With Memory:
→ Genres: indie, alternative (biased by history)
→ Tracks: Bon Iver, Radiohead, The National
→ Still matches rainy/melancholic vibe!
```

**The Critic's Role:**
- Prevents over-personalization: Won't recommend jazz for a metal scene just because you like jazz
- Validates narrative fit: "This track is technically correct but contextually wrong" → Rejected
- Explains reasoning: "Nightcall by Kavinsky captures the neon-soaked urban isolation perfectly"

## 🎯 Use Cases

### For Content Creators
- Upload video thumbnail → Get soundtrack suggestions
- Match music to visual aesthetic automatically
- Build mood-based playlists for different scenes

### For Music Discovery
- "Show me music that matches this sunset photo"
- Learn your taste through likes
- Get personalized recommendations based on visual vibes

### For Developers
- Example of production-ready LangGraph agents
- Multimodal AI integration patterns
- Hybrid search (API + vector DB) implementation
- A/B testing infrastructure for ML systems

## 📊 Example Interactions

### Scenario 1: First Time User (Cold Start)
```
User: [Uploads photo of rainy city street at night]

Vision Agent: 
→ "Neon-lit urban solitude, melancholic yet energetic"
→ No user history available
→ Parameters: valence=0.3, energy=0.6, acousticness=0.2
→ Genres: electronic, synth-pop

Search Agent: 
→ Queries Spotify Recommendations API
→ Finds 15 candidates

Curator Agent: 
→ Filters to 5 tracks
→ "Nightcall by Kavinsky - Captures the neon-soaked urban isolation perfectly"
→ "Midnight City by M83 - Energetic yet introspective, matches the vibe"

User: Likes 2 tracks (Kavinsky, M83)
→ Saved to user_likes.json
→ System now knows: User likes electronic, synth-pop
```

### Scenario 2: Returning User (Warm Start with Memory)
```
User: [Uploads photo of cozy cafe]

Vision Agent:
→ Reads user history: "User likes: Kavinsky, M83, The Midnight"
→ "Warm, intimate, acoustic setting"
→ Biases towards user's electronic taste BUT respects acoustic context
→ Parameters: valence=0.7, energy=0.4, acousticness=0.6
→ Genres: chillwave, indie-electronic (hybrid of user taste + scene)

Search Agent:
→ Finds 15 tracks blending electronic + acoustic

Curator Agent:
→ Validates: "Tycho fits—electronic but organic"
→ Rejects: "Deadmau5 too aggressive for cafe vibe"
→ Top 5: Tycho, Bonobo, Ólafur Arnalds

User: "Make it more upbeat"
→ Vision Agent re-analyzes with feedback
→ energy=0.6 (increased)
→ Returns new recommendations
```

### Scenario 3: The Critic Prevents Hallucinations
```
Photo: Sleeping baby in nursery

Vision Agent:
→ "Peaceful, gentle, lullaby-like"
→ Parameters: valence=0.8, energy=0.1, acousticness=0.9
→ Genres: ambient, classical

Search Agent:
→ Returns 15 tracks including:
  - "Clair de Lune" (perfect)
  - "Thunderstruck" by AC/DC (Spotify glitch—high acousticness guitar?)

Curator Agent (The Critic):
→ Reviews: "Thunderstruck for a sleeping baby? REJECTED"
→ Filters out mismatches
→ Keeps only contextually appropriate tracks
→ Explains: "Clair de Lune's gentle piano perfectly soothes the nursery atmosphere"
```

## 🔬 Technical Highlights

### Why This Architecture Wins

**1. True Agentic Behavior**
- Not just API chaining—each agent has a specific role and reasoning process
- State machine allows for complex workflows and loops
- Agents critique and validate each other's outputs (The Curator prevents Vision Agent hallucinations)
- Multi-step reasoning: Vision → Search → Critique → Explain

**2. Multimodal Intelligence**
- Gemini 3 Flash processes images AND text in the same model
- Extracts abstract concepts (mood, narrative) from pixels
- Translates visual aesthetics to audio parameters
- Understands implied context: "3 AM loneliness" from a photo of an empty street

**3. The Critic (Quality Control)**
- **Prevents Hallucinations**: Catches when AI recommends contextually wrong tracks
- **Validates Spotify Results**: Technical correctness ≠ contextual fit
- **Example**: Spotify returns "Thunderstruck" for a lullaby scene (high acousticness guitar) → Curator rejects it
- **Explainable AI**: Every recommendation comes with reasoning
- **Match Scoring**: Ranks tracks by narrative alignment (0-100)

**4. Reinforcement Learning Lite**
- **Implicit Feedback**: Likes train the system without explicit ratings
- **Persistent Memory**: User preferences stored across sessions
- **Context-Aware Learning**: Balances user taste with photo context
- **Adaptive Recommendations**: System improves with every interaction
- **No Cold Start Problem**: Works great for first-time users, gets better over time

**5. Production-Ready**
- Stateless backend (sessions in memory/DB)
- Containerized for cloud deployment
- Error handling and fallbacks throughout
- Valid genre seeds (no Spotify API errors)
- Token refresh for long-running sessions

## 🧪 Future Enhancements

**Vector Embeddings (Coming Soon)**
- Semantic search across liked tracks using Vectra
- "Find tracks that *feel* like my favorites"
- Hybrid ranking: Spotify + Vector similarity

**Multi-tab Interface (In Progress)**
- Tab 1: Photo Upload (current)
- Tab 2: My Playlists (liked tracks organized by vibe)
- Tab 3: Dashboard (stats, top artists, listening patterns)

**Audio Feature Profiling**
- Calculate average danceability, energy, valence from liked tracks
- Boost candidates matching your audio profile
- Visualize your musical DNA

**A/B Testing Infrastructure**
- Track metrics for experimentation
- Compare RL-enhanced vs basic recommendations
- Optimize for user engagement

## 🤝 Contributing

This project was built for the Gemini 3 Global Hackathon. Contributions welcome!

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt
npm install --save-dev

# Run tests
pytest backend/tests/
npm test

# Format code
black backend/
prettier --write frontend/
```

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Google DeepMind for Gemini 3 API
- Spotify for their excellent Web API
- LangChain team for LangGraph
- The open-source community

---

*Built for the Gemini 3 Global Hackathon*

**Demo**: [Coming Soon]  
**Video**: [Coming Soon]  
**Slides**: [Coming Soon]
