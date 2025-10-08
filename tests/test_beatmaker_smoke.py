from pathlib import Path
from agents.beatmaker.beatmaker_agent import generate_midi, make_filename

def test_generate_mid(tmp_path: Path):
    params = dict(bars=2, tempo_bpm=90, key="A", scale="minor", style="lofi", seed=42)
    out = tmp_path/"test.mid"
    p = generate_midi(params, out)
    assert p.exists() and p.stat().st_size > 0
