'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Refinement State
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [refineText, setRefineText] = useState("");
  const [isRefining, setIsRefining] = useState(false);
  const [likedTracks, setLikedTracks] = useState<Set<string>>(new Set());

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setSessionId(null);
      setRefineText("");
      setLikedTracks(new Set());
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setResult(null);
    setSessionId(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedImage);

      // Use env var or default to localhost
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://muse-backend-2vu4yee5ha-uc.a.run.app';
      const response = await fetch(`${apiUrl}/analyze-photo`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
      setSessionId(data.session_id);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async () => {
    if (!sessionId || !refineText) return;

    setIsRefining(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://muse-backend-2vu4yee5ha-uc.a.run.app';
      const response = await fetch(`${apiUrl}/refine`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          feedback: refineText
        }),
      });

      const data = await response.json();
      setResult(data); // Update results with new refined data
      setRefineText(""); // Clear input
    } catch (error) {
      console.error('Refine Error:', error);
    } finally {
      setIsRefining(false);
    }
  };

  const handleLike = async (track: any) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://muse-backend-2vu4yee5ha-uc.a.run.app';
      await fetch(`${apiUrl}/like-track`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          track_id: track.id,
          track_name: track.name,
          artist_name: track.artist
        })
      });
      setLikedTracks(prev => {
        const newSet = new Set(prev);
        newSet.add(track.id);
        return newSet;
      });
    } catch (e) {
      console.error("Failed to like track", e);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

      <main className="z-10 w-full max-w-5xl flex flex-col items-center gap-8">
        <h1 className="text-6xl font-black bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">
          Muse.AI
        </h1>
        <p className="text-xl text-slate-400 text-center max-w-2xl">
          Upload a photo. Let AI analyze the vibe. Discover the perfect soundtrack.
        </p>

        {/* Upload Section */}
        <div className="w-full bg-slate-900/50 backdrop-blur-md rounded-2xl p-6 border border-slate-800 shadow-2xl">
          <div className="flex flex-col items-center gap-4">
            {previewUrl ? (
              <div className="relative w-full max-w-md">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="w-full h-64 object-cover rounded-lg"
                />
                <button
                  onClick={() => {
                    setSelectedImage(null);
                    setPreviewUrl(null);
                    setResult(null);
                  }}
                  className="absolute top-2 right-2 bg-red-500/80 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm"
                >
                  Remove
                </button>
              </div>
            ) : (
              <label className="w-full max-w-md h-64 flex flex-col items-center justify-center border-2 border-dashed border-slate-700 rounded-lg cursor-pointer hover:border-cyan-500 transition-colors">
                <div className="flex flex-col items-center gap-2">
                  <svg className="w-12 h-12 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span className="text-slate-400">Click to upload photo</span>
                  <span className="text-xs text-slate-600">JPG, PNG, or GIF</span>
                </div>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageSelect}
                  className="hidden"
                />
              </label>
            )}

            <div className="w-full flex justify-between items-center">
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-900/50 text-blue-300 border border-blue-800">
                ✨ Powered by Gemini 3 + Spotify
              </span>

              <button
                onClick={handleAnalyze}
                disabled={loading || !selectedImage}
                className={`px-8 py-3 rounded-xl font-bold text-lg transition-all ${loading || !selectedImage
                  ? 'bg-slate-700 cursor-not-allowed'
                  : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-105 shadow-lg shadow-cyan-500/20'
                  }`}
              >
                {loading ? 'Analyzing...' : 'Find My Soundtrack'}
              </button>
            </div>
          </div>
        </div>

        {result && (
          <div className="w-full animate-fade-in-up pb-20">
            {/* Vibe Analysis */}
            <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-700 mb-6">
              <h3 className="text-2xl font-bold text-white mb-3">Vibe Analysis</h3>
              <p className="text-slate-300 text-lg italic mb-6">"{result.vibe_analysis}"</p>

              {/* Tech Stats (Search Params) */}
              {result.search_parameters && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  {Object.entries(result.search_parameters).map(([key, value]) => {
                    if (key.startsWith("target_") && typeof value === 'number') {
                      return (
                        <div key={key} className="bg-slate-800 p-3 rounded-lg border border-slate-700">
                          <p className="text-xs text-slate-500 uppercase font-bold">{key.replace("target_", "")}</p>
                          <div className="flex items-end gap-2">
                            <span className="text-xl font-mono text-cyan-400">{value}</span>
                            <div className="w-full bg-slate-700 h-2 rounded-full mb-1">
                              <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${value * 100}%` }}></div>
                            </div>
                          </div>
                        </div>
                      )
                    }
                    return null;
                  })}
                </div>
              )}
            </div>

            {/* Refine / Feedback Section */}
            <div className="bg-gradient-to-r from-purple-900/40 to-cyan-900/40 border border-slate-700 p-4 rounded-xl mb-8 flex gap-4 items-center">
              <div className="flex-1">
                <p className="text-sm font-bold text-cyan-300 mb-1">🤖 Agent Feedback Loop</p>
                <input
                  type="text"
                  placeholder="e.g. 'Too sad, make it more energetic' or 'I want 80s vibes'"
                  className="w-full bg-slate-900/50 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyan-500"
                  value={refineText}
                  onChange={(e) => setRefineText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRefine()}
                />
              </div>
              <button
                onClick={handleRefine}
                disabled={isRefining || !refineText}
                className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-6 py-2 rounded-lg h-10 mt-6 disabled:opacity-50"
              >
                {isRefining ? 'Refining...' : 'Refine'}
              </button>
            </div>

            {/* Track Recommendations */}
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-white">Curated Selection</h3>
              {result.recommendations.map((rec: any, idx: number) => (
                <div key={idx} className="bg-slate-900/80 rounded-xl p-5 border border-slate-700 hover:border-cyan-500/50 transition-all group">
                  <div className="flex gap-4 items-start">
                    {/* Index + Score */}
                    <div className="flex flex-col items-center gap-1 min-w-[3rem]">
                      <span className="text-2xl font-black text-slate-700 group-hover:text-cyan-600/50">#{idx + 1}</span>
                      {rec.match_score && (
                        <span className="text-xs font-mono bg-green-900/50 text-green-400 px-2 py-0.5 rounded border border-green-800">
                          {rec.match_score}%
                        </span>
                      )}
                    </div>

                    {rec.track.image && (
                      <img
                        src={rec.track.image}
                        alt={rec.track.name}
                        className="w-20 h-20 rounded-lg object-cover shadow-lg"
                      />
                    )}
                    <div className="flex-1">
                      <h4 className="text-lg font-bold text-white">{rec.track.name}</h4>
                      <p className="text-slate-400 text-sm mb-2">{rec.track.artist}</p>

                      <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700/50 mb-3">
                        <p className="text-cyan-200 text-sm italic">
                          <span className="text-cyan-500 font-bold not-italic">AI Reason: </span>
                          "{rec.explanation}"
                        </p>
                      </div>

                      <div className="flex gap-3">
                        <button
                          onClick={() => handleLike(rec.track)}
                          disabled={likedTracks.has(rec.track.id)}
                          className={`p-2 rounded-full border transition-all ${likedTracks.has(rec.track.id)
                              ? 'bg-red-500/20 border-red-500 text-red-500'
                              : 'border-slate-600 text-slate-400 hover:border-red-400 hover:text-red-400'
                            }`}
                          title="Like this track to improve future recommendations"
                        >
                          <svg className="w-5 h-5" fill={likedTracks.has(rec.track.id) ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                        </button>

                        <a
                          href={rec.track.spotify_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-4 py-2 bg-[#1DB954] hover:bg-[#1ed760] text-black rounded-full text-sm font-bold transition-colors flex items-center gap-2"
                        >
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141 4.32-1.38 9.841-.72 13.561 1.56.42.24.6.72.18 1.26zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" /></svg>
                          Play on Spotify
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
