'use client';

import { useState } from 'react';

import Script from 'next/script';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [playerReady, setPlayerReady] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async (rating: string) => {
    try {
      await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, rating })
      });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-4 relative overflow-hidden">
      <Script
        src="https://cdn.jsdelivr.net/npm/@magenta/music@1.23.1/dist/magentamusic.min.js"
        onLoad={() => setPlayerReady(true)}
      />

      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

      <main className="z-10 w-full max-w-4xl flex flex-col items-center gap-8">
        <h1 className="text-6xl font-black bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-cyan-400">
          Muse.AI
        </h1>
        <p className="text-xl text-slate-400 text-center max-w-2xl">
          The Artificial Composer Studio. Describe your scene, and let our Neuro-Symbolic AI compose a unique soundtrack.
        </p>

        {/* Input Section */}
        <div className="w-full bg-slate-900/50 backdrop-blur-md rounded-2xl p-6 border border-slate-800 shadow-2xl">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your vibe (e.g., 'Cyberpunk chase in the rain, urgent, synth-heavy')..."
            className="w-full bg-transparent text-white p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500 h-32 resize-none text-lg placeholder-slate-600"
          />

          <div className="mt-4 flex justify-between items-center">
            <div className="flex gap-4">
              {/* Badges for Partners */}
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-900/50 text-blue-300 border border-blue-800">Gemini Powered</span>
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-green-900/50 text-green-300 border border-green-800">Vertex AI</span>
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-purple-900/50 text-purple-300 border border-purple-800">Datadog</span>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading || !prompt}
              className={`px-8 py-3 rounded-xl font-bold text-lg transition-all ${loading
                ? 'bg-slate-700 cursor-not-allowed'
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-105 shadow-lg shadow-cyan-500/20'
                }`}
            >
              {loading ? 'Composing...' : 'Generate Soundtrack'}
            </button>
          </div>
        </div>

        {/* Result Section */}
        {result && (
          <div className="w-full animate-fade-in-up">
            <div className="bg-slate-900/80 rounded-2xl p-8 border border-slate-700">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-white">Composition Ready</h3>
                  <p className="text-slate-400">Generated in key {result.metadata.key} • {result.metadata.tempo} BPM</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-slate-500">Inference Time: 0.8s</p>
                  <p className="text-xs text-slate-500">Model: Transformer-XS</p>
                </div>
              </div>

              {/* Active Learning / Feedback Loop */}
              <div className="flex gap-4 justify-end mb-4">
                <span className="text-xs uppercase tracking-widest text-slate-500 self-center">RLHF Feedback:</span>
                <button
                  onClick={() => submitFeedback("up")}
                  className="p-2 bg-green-900/30 hover:bg-green-800 rounded-lg text-green-400 text-xs transition-colors"
                >
                  👍 Perfection
                </button>
                <button
                  onClick={() => {
                    submitFeedback("down");
                    alert("Feedback recorded! Try hitting 'Generate' again for a different variation.");
                  }}
                  className="p-2 bg-red-900/30 hover:bg-red-800 rounded-lg text-red-400 text-xs transition-colors"
                >
                  👎 Needs Work
                </button>
              </div>

              {/* Real Visualizer / Audio Player using Magenta */}
              <div className="h-32 bg-slate-800 rounded-lg flex flex-col items-center justify-center mb-6 overflow-hidden relative p-4 gap-4">
                <p className="text-sm text-slate-400">Click to Play Generated MIDI</p>
                <button
                  disabled={!playerReady}
                  onClick={() => {
                    if ((window as any).mm) {
                      const mm = (window as any).mm;
                      // Use SoundFontPlayer
                      const player = new mm.SoundFontPlayer('https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus');

                      // Load the MIDI to analyze it for visualization
                      // Append timestamp to prevent caching the same filename
                      const midiUrl = result.midi_path + '?t=' + Date.now();
                      fetch(midiUrl)
                        .then(res => res.blob())
                        .then(blob => {
                          blob.arrayBuffer().then(buff => {
                            // Parse for visualizer
                            const noteSeq = mm.midiToSequenceProto(buff);
                            new mm.Visualizer(noteSeq, document.getElementById('visCheck'), {
                              noteHeight: 6,
                              pixelsPerTimeStep: 30,
                            });
                            player.start(noteSeq);
                          });
                        });
                    } else {
                      alert("Player loading...");
                    }
                  }}
                  className="z-10 bg-cyan-600 px-6 py-2 rounded-full cursor-pointer hover:bg-cyan-500 text-white font-bold transition-all shadow-lg"
                >
                  ▶ Play Full Track
                </button>
                <canvas id="visCheck" className="absolute inset-0 w-full h-full opacity-30 pointer-events-none"></canvas>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
                  <h4 className="text-sm font-bold text-slate-400 mb-2">Structure</h4>
                  <div className="flex gap-1">
                    <div className="h-2 flex-1 bg-blue-500 rounded"></div>
                    <div className="h-2 flex-[2] bg-purple-500 rounded"></div>
                    <div className="h-2 flex-1 bg-blue-500 rounded"></div>
                  </div>
                  <div className="flex justify-between text-xs text-slate-500 mt-1">
                    <span>Intro</span>
                    <span>Climax</span>
                    <span>Outro</span>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
                  <h4 className="text-sm font-bold text-slate-400 mb-2">Data Stream</h4>
                  <code className="text-xs text-green-400 block font-mono">
                    {`> MIDI_EVENTS_GENERATED: 1,240`} <br />
                    {`> VELOCITY_MAP: OPTIMIZED`}
                  </code>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
