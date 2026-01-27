'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;
    
    setLoading(true);
    setResult(null);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedImage);
      
      const response = await fetch('http://localhost:8000/analyze-photo', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
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
                className={`px-8 py-3 rounded-xl font-bold text-lg transition-all ${
                  loading || !selectedImage
                    ? 'bg-slate-700 cursor-not-allowed'
                    : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-105 shadow-lg shadow-cyan-500/20'
                }`}
              >
                {loading ? 'Analyzing...' : 'Find My Soundtrack'}
              </button>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="w-full animate-fade-in-up">
            {/* Vibe Analysis */}
            <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-700 mb-6">
              <h3 className="text-2xl font-bold text-white mb-3">Vibe Analysis</h3>
              <p className="text-slate-300 mb-4">{result.vibe_analysis.scene_description}</p>
              <div className="flex gap-2 flex-wrap">
                <span className="px-3 py-1 bg-purple-900/50 text-purple-300 rounded-full text-sm">
                  {result.vibe_analysis.mood}
                </span>
                <span className="px-3 py-1 bg-cyan-900/50 text-cyan-300 rounded-full text-sm">
                  {result.vibe_analysis.genre}
                </span>
                <span className="px-3 py-1 bg-pink-900/50 text-pink-300 rounded-full text-sm">
                  {result.vibe_analysis.tempo} tempo
                </span>
                {result.vibe_analysis.keywords.map((kw: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-slate-800 text-slate-400 rounded-full text-sm">
                    {kw}
                  </span>
                ))}
              </div>
            </div>

            {/* Track Recommendations */}
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-white">Perfect Matches</h3>
              {result.recommendations.map((rec: any, idx: number) => (
                <div key={idx} className="bg-slate-900/80 rounded-xl p-5 border border-slate-700 hover:border-cyan-500/50 transition-all">
                  <div className="flex gap-4">
                    {rec.track.image && (
                      <img 
                        src={rec.track.image} 
                        alt={rec.track.name}
                        className="w-20 h-20 rounded-lg object-cover"
                      />
                    )}
                    <div className="flex-1">
                      <h4 className="text-lg font-bold text-white">{rec.track.name}</h4>
                      <p className="text-slate-400 text-sm mb-2">{rec.track.artist} • {rec.track.album}</p>
                      <p className="text-cyan-200 text-sm italic mb-3">"{rec.explanation}"</p>
                      <div className="flex gap-3">
                        <a 
                          href={rec.track.spotify_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded-lg text-sm font-bold transition-colors"
                        >
                          Open in Spotify
                        </a>
                        {rec.track.preview_url && (
                          <button
                            onClick={() => {
                              const audio = new Audio(rec.track.preview_url);
                              audio.play();
                            }}
                            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition-colors"
                          >
                            ▶ Preview
                          </button>
                        )}
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
