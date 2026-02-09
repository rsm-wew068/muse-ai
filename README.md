# 🎵 Muse.AI: The Agentic Music Curator
> **Built for the Google DeepMind Gemini 3 Hackathon** 
> *Leveraging Gemini 3 Preview, LangGraph, and Google Cloud Run.*



## 💡 The Problem
We all have moments we want to share—a rainy night drive, a crowded cyberpunk street, a quiet coffee morning. But finding the *exact* song that matches that visual vibe is frustrating. Keyword search ("sad songs") returns generic pop hits, not the deep cuts that truly fit the narrative.

## 🚀 The Solution: Agentic Reasoning
Muse.AI isn't just a wrapper. It's a **Multi-Agent System** that "sees" your photo, formulates a search strategy, scouts for candidates, and then *critiques* them like a human DJ.

---


## 🧠 The "Muse" Agent Architecture

Muse.AI uses a **LangGraph-based state machine** with specialized agents that work together, validate each other, and learn from your feedback:

### The Agent Pipeline

1.  **👁️ The Visionary (Gemini 3 Flash - Multimodal)**
    *   **What it does**: Analyzes photos beyond objects—captures lighting, mood, texture, and implied narrative
    *   **Output**: Poetic "Scene Narrative" (e.g., "solitude at 3 AM, neon-lit streets") + precise audio targets
    *   **Audio Parameters**: Valence (happiness), Energy (intensity), Acousticness, Danceability
    *   **Memory Integration**: Reads your liked tracks history and subtly biases towards your preferred genres *while still respecting the visual context*
    *   **Feedback Aware**: "Make it more upbeat" → recalibrates valence/energy parameters

2.  **🎼 The Musicologist (Smart Search)**
    *   **Smart Query Translation**: Converts abstract audio parameters (low energy, sad) into search phrases (`indie chill`)
    *   **Spotify Search API**: Uses the Search endpoint to retrieve candidates
    *   **Multi-Query Fan-Out**: Runs multiple search queries per photo for higher recall
    *   **Output**: Up to 30 candidate tracks, then reranked by the Curator

3.  **⚖️ The Curator (Gemini 3 Flash - The Critic)**
    *   **What it does**: Acts as quality control—reviews candidates against the scene narrative
    *   **Filters Hallucinations**: *"Does Death Metal fit a Sleeping Baby photo?"* → **Rejected**
    *   **Prevents Mismatches**: Catches when Spotify returns technically correct but contextually wrong tracks
    *   **Explains Reasoning**: Generates creative 1-sentence explanations for each recommendation
    *   **Output**: Top 5 tracks with match scores and explanations

4.  **🧠 Long-Term Memory (Reinforcement Learning Lite)**
    *   **Learns Your Taste**: Every "Like" builds your musical profile
    *   **Persistent Preferences**: Stored in **Firestore** across sessions
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
*   **Audio Feature Mapping**: Translates visual vibes into search-friendly parameters and queries
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
*   **Real-time Stats**: Track your top artists via the /stats endpoint
*   **Cloud Deployment**: Containerized and ready for Google Cloud Run
*   **API-First Design**: RESTful endpoints for integration

## 🛠️ Tech Stack

### AI & Agent Framework
*   **Google Gemini 3 Flash Preview**: Multimodal vision analysis + text generation/reasoning
*   **LangGraph**: Stateful agent orchestration and workflow management
*   **Spotify Web API**: Search API for track retrieval

### Application Stack
*   **Frontend**: Next.js 16 (React 19) + TailwindCSS v4 + Glassmorphism UI
*   **Backend**: FastAPI (Python 3.11+) + Pydantic for type safety
*   **Storage**: Firestore (per-user likes)
*   **Infrastructure**: Docker + Google Cloud Run with auto-scaling

### Key Libraries
*   `langgraph` - Agent state machine
*   `google-generativeai` - Gemini API client
*   `google-cloud-firestore` - Per-user memory storage
*   `requests` - Spotify Web API integration
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

# Install dependencies (includes LangGraph, FastAPI)
pip install -r requirements.txt

# Run the Agent API
python main.py
```

*Backend runs on `http://localhost:8000`*

**API Endpoints:**
- `POST /analyze-photo` - Upload photo, get recommendations (expects `user_id` in form data)
- `POST /refine` - Provide feedback to refine results (expects `user_id`)
- `POST /like-track` - Save track to your favorites (expects `user_id`)
- `GET /stats` - Get your listening stats (Top Artists) via `?user_id=...`
- `GET /playlists` - Get playlists grouped by query via `?user_id=...`


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
6. Explore Playlists and Stats in the UI tabs

## ☁️ Deployment (Google Cloud Run)

Deploy both frontend and backend as auto-scaling serverless containers:

### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed locally

### Continuous Deployment (GitOps)

This project includes a **GitHub Actions** workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys to Google Cloud Run whenever you push to the `main` branch.

1.  Connect your GitHub repository.
2.  Add GCP Secrets to GitHub Settings (`GCP_SA_KEY`, `GEMINI_API_KEY`, etc.).
3.  Push to `main`.
4.  Monitor progress in the "Actions" tab.

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
    │ 2. SEARCH NODE (Smart Query Agent)      │
    │    - Translates vibes to Search Queries │
    │      (e.g., "indie melancholic")        │
    │    - Uses Spotify Search API            │
    │    - Multi-query fan-out                │
    │    - Output: up to 30 candidates        │
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
    search_queries: list                 # ["indie melancholic", "late night synth"]
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
- Query fan-out + LLM reranking implementation
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
→ Queries Spotify Search API
→ Finds up to 30 candidates

Curator Agent: 
→ Filters to 5 tracks
→ "Nightcall by Kavinsky - Captures the neon-soaked urban isolation perfectly"
→ "Midnight City by M83 - Energetic yet introspective, matches the vibe"

User: Likes 2 tracks (Kavinsky, M83)
→ Saved to Firestore
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
→ Finds up to 30 tracks blending electronic + acoustic

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
→ Returns candidates including:
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
- Token refresh for long-running sessions

## 🧪 Future Enhancements

**Vector Embeddings (Coming Soon)**
- Semantic search across liked tracks using a vector store
- "Find tracks that *feel* like my favorites"
- Hybrid ranking: Spotify + Vector similarity

**Multi-tab Interface**
- Tab 1: Assistant (photo → recommendations)
- Tab 2: Playlists (liked tracks grouped by query)
- Tab 3: Stats (top artists, listening patterns)

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
