import numpy as np
from music21 import stream, note, chord

class MusicEvaluator:
    @staticmethod
    def evaluate_piece(score: stream.Score) -> dict:
        """
        Evaluates a music21 Score using metrics inspired by CSE 253 Homework 1.
        """
        notes = []
        for element in score.recurse():
            if isinstance(element, note.Note):
                notes.append(element)
            elif isinstance(element, chord.Chord):
                # For chords, consider the root note for statistics or all notes?
                # Let's take the root for pitch stats.
                notes.append(note.Note(element.root()))

        if not notes:
            return {
                "pitch_range": 0,
                "unique_pitch_count": 0,
                "average_pitch": 0,
                "note_density": 0,
                "evaluation_summary": "Empty Track"
            }

        pitches = [n.pitch.ps for n in notes]  # .ps is midi pitch number as float

        # --- Metrics from Homework 1 ---
        # 1. get_lowest_pitch / get_highest_pitch -> Range
        min_p = min(pitches)
        max_p = max(pitches)
        pitch_range = max_p - min_p

        # 2. get_unique_pitch_num
        unique_pitch_count = len(set(pitches))

        # 3. get_average_pitch_value
        average_pitch = np.mean(pitches)

        # 4. featureQ10 (Note Density)
        # Approximate duration in seconds (assuming 120 BPM if not specified, 
        # but the score has duration in quarter notes)
        total_duration_quarters = score.duration.quarterLength
        # Assuming 120 BPM for normalization visualization if specific tempo map is missing
        # Duration in seconds = quarters * (60 / bpm)
        # Let's just use "Notes per Quarter Length" as a robust metric
        note_density = len(notes) / total_duration_quarters if total_duration_quarters > 0 else 0

        # --- Interpretation ---
        summary = []
        if note_density > 2.0:
            summary.append("High Energy (Virtuoso)")
        elif note_density > 1.0:
            summary.append("Moderate Flow")
        else:
            summary.append("Sparse / Ambient")

        if unique_pitch_count > 12:
            summary.append("Chromatically Rich")
        elif unique_pitch_count < 5:
            summary.append("Minimalist")
        else:
            summary.append("Diatonic / Stable")

        return {
            "pitch_range": int(pitch_range),
            "unique_pitch_count": unique_pitch_count,
            "average_pitch": round(average_pitch, 1),
            "note_density": round(note_density, 2),
            "evaluation_summary": " • ".join(summary)
        }
