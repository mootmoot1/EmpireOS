#!/usr/bin/env python3
import argparse, os, json
from pathlib import Path
from datetime import datetime

# import our generator
from agents.beatmaker.beatmaker_agent import generate_midi, make_filename, DEFAULTS

def song_folder(root: Path, song: str) -> Path:
    d = root / "outputs" / "beatmaker" / song
    d.mkdir(parents=True, exist_ok=True)
    return d

def main():
    p = argparse.ArgumentParser(description="BeatMaker – generate MIDI layers")
    p.add_argument("--style", default=DEFAULTS["style"])
    p.add_argument("--key",   default=DEFAULTS["key"])
    p.add_argument("--bpm",   type=int, default=DEFAULTS["bpm"])
    p.add_argument("--bars",  type=int, default=DEFAULTS["bars"])
    p.add_argument("--song",  required=True, help="Song name (folder)")
    p.add_argument("--layers", default="drums,chords,melody",
                   help="Comma list of layers to render")
    args = p.parse_args()

    root = Path(__file__).resolve().parents[1]
    outdir = song_folder(root, args.song)

    # save a small manifest for convenience
    manifest = {
        "song": args.song,
        "style": args.style,
        "key": args.key,
        "bpm": args.bpm,
        "bars": args.bars,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    made = []
    for layer in [s.strip() for s in args.layers.split(",") if s.strip()]:
        fname = make_filename(f"{args.style}-{layer}", args.key, args.bpm, args.bars)
        outpath = outdir / fname
        # you can branch layer-specific logic inside generate_midi if you want
        generate_midi(args.style, args.key, args.bpm, args.bars, str(outpath))
        made.append(outpath.name)

    print(f"✅ Saved to: {outdir}")
    print("🎼 Files:", *made, sep="\n  - ")

if __name__ == "__main__":
    main()

