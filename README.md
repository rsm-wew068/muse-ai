# Muse.AI 🎵
> *Photo to Music: AI-Powered Soundtrack Discovery*

**Muse.AI** analyzes the vibe of your photos and recommends the perfect Spotify tracks to match. Using Gemini 2.0's vision capabilities and Spotify's vast music library, it creates a personalized soundtrack for any moment captured in an image.

## 🚀 How It Works

1. **Upload a Photo**: Any image - a sunset, city street, cozy cafe, or adventure scene
2. **AI Vision Analysis**: Gemini 2.0 Flash analyzes the mood, energy, and aesthetic
3. **Spotify Search**: Finds tracks that match the vibe using intelligent keyword mapping
4. **AI Explanations**: Gemini Flash explains why each track perfectly captures your photo's essence

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (React 19)
- **Styling**: TailwindCSS v4 with Glassmorphism UI
- **Image Upload**: Native file input with preview

### Backend
- **API**: FastAPI
- **Vision AI**: Google Gemini 3 Flash Preview (multimodal)
- **Music API**: Spotify Web API
- **Explainer AI**: Google Gemini 3 Flash Preview (text generation)

## ⚡️ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Gemini API Key
- Spotify API Credentials

### 1. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up Environment Variables
# Create .env file in project root with:
GEMINI_API_KEY=your_gemini_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Run the API
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

1. **Image Upload**: User uploads photo via browser
2. **Vision Analysis**: Gemini 3 Flash Preview extracts mood, genre, tempo, keywords, and scene description
3. **Spotify Search**: Query built from vibe analysis to find matching tracks
4. **AI Explanation**: For each track, Gemini 3 Flash Preview explains the connection to the photo's vibe
5. **Results Display**: Shows tracks with album art, preview links, and AI-generated explanations
