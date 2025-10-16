#!/usr/bin/env python3
"""
BeatMaker CLI — generates MIDI stems into a neat song folder.
- No FluidSynth usage (audio rendering skipped).
- Optional: reveal the output folder in Finder (macOS).
"""

from pathlib import Path
import argparse, json, time, subprocess, sys

# Reuse MIDI generator from the agent
from agents.beatmaker.beatmaker_agent import generate_midi, DEFAULTS

def make_filename(stem: str, key: str, bpm: int, bars: int, ts: str) -> str:
    return f"{stem}_{key}_{bpm}bpm_{bars}bars_{ts}.mid"

def main():
    p = argparse.ArgumentParser(description="BeatMaker -> generate a MIDI stem bundle")
    p.add_argument("--style",  default="trap",        help="style tag (e.g. trap, lofi, drill)")
    p.add_argument("--key",    default=DEFAULTS.get("key","C_minor"))
    p.add_argument("--bpm",    type=int, default=DEFAULTS.get("tempo_bpm",140))
    p.add_argument("--bars",   type=int, default=DEFAULTS.get("bars",8))
    p.add_argument("--song",   default="Untitled")
    p.add_argument("--reveal", action="store_true", help="Open the output folder in Finder when done")
    args = p.parse_args()

    # Output layout: outputs/beatmaker/<SongName>/<timestamp>/
    root = Path("outputs/beatmaker")
    ts   = time.strftime("%Y%m%d_%H%M%S")
    folder = root / args.song / ts
    folder.mkdir(parents=True, exist_ok=True)

    stems = ["drums","chords","melody"]  # extend later (bass, counter, fx, etc.)
    written = []

    for stem in stems:
        mid = generate_midi(stem=stem, key=args.key, tempo=args.bpm, bars=args.bars, style=args.style)
        out_name = make_filename(stem, args.key, args.bpm, args.bars, ts)
        out_path = folder / out_name
        mid.save(out_path)
        written.append(out_name)

    # Manifest for DAW import
    manifest = {
        "song": args.song,
        "style": args.style,
        "key": args.key,
        "bpm": args.bpm,
        "bars": args.bars,
        "timestamp": ts,
        "files": written,
        "notes": "Render audio in your DAW (FL/Logic). FluidSynth intentionally disabled."
    }
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print("✅ Beat created:")
    print("   Folder:", str(folder.resolve()))
    print("   Files:", *written, sep="\n   - ")

    if args.reveal and sys.platform == "darwin":
        # Open folder in Finder
        try:
            subprocess.run(["open", str(folder.resolve())], check=False)
        except Exception as e:
            print(f"⚠️ Could not reveal folder: {e}")

if __name__ == "__main__":
    main()
