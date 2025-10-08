#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from agents.beatmaker.beatmaker_agent import generate_midi, make_filename, DEFAULTS

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bars", type=int, default=DEFAULTS["bars"])
    p.add_argument("--bpm", type=int, default=DEFAULTS["tempo_bpm"])
    p.add_argument("--key", type=str, default=DEFAULTS["key"])
    p.add_argument("--scale", type=str, default=DEFAULTS["scale"])
    p.add_argument("--style", type=str, default=DEFAULTS["style"])
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    params = dict(bars=args.bars, tempo_bpm=args.bpm, key=args.key, scale=args.scale, style=args.style, seed=args.seed)
    out = make_filename(params)
    path = generate_midi(params, out)
    print(f"✅ Generated: {path}")

if __name__ == "__main__":
    main()
