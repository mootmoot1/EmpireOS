from pathlib import Path
from typing import Dict, List
import random
import time

try:
    from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
except Exception as e:
    raise RuntimeError("Missing dep: mido. Add to requirements.txt. Error: %r" % e)

DEFAULTS = {
    "bars": 8,
    "tempo_bpm": 84,
    "key": "A",
    "scale": "minor",   # minor|major|dorian
    "style": "lofi",    # lofi|trap|drill|boom-bap
    "seed": None
}

KEY_TO_SEMITONE = {"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"F":5,"F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11}
SCALES = {
    "minor":  [0,2,3,5,7,8,10],
    "major":  [0,2,4,5,7,9,11],
    "dorian": [0,2,3,5,7,9,10],
}

DRUMS = {
    "kick": 36,   # C1
    "snare": 38,  # D1
    "hat": 42,    # F#1 (closed hat)
}

def _key_root(key: str) -> int:
    key = key.strip().title()
    if key not in KEY_TO_SEMITONE: key = "A"
    return 60 + KEY_TO_SEMITONE[key]  # C4 is 60

def _scale_notes(root: int, scale: str) -> List[int]:
    degrees = SCALES.get(scale, SCALES["minor"])
    # two octaves for variety
    return [root + d + 12*o for o in (0,1) for d in degrees]

def _style_params(style: str):
    style = (style or "lofi").lower()
    if style == "trap":
        return dict(kick_pat=[1,0,0,0], snr_pat=[0,0,1,0], hat_density=4, velocity=96)
    if style == "drill":
        return dict(kick_pat=[1,0,1,0], snr_pat=[0,0,1,0], hat_density=6, velocity=100)
    if style == "boom-bap":
        return dict(kick_pat=[1,0,0,0], snr_pat=[0,0,1,0], hat_density=2, velocity=90)
    # lofi default
    return dict(kick_pat=[1,0,0,0], snr_pat=[0,0,1,0], hat_density=3, velocity=80)

def generate_midi(params: Dict, out_path: Path) -> Path:
    cfg = {**DEFAULTS, **(params or {})}
    if cfg["seed"] is not None:
        random.seed(cfg["seed"])

    bars       = int(cfg["bars"])
    tempo_bpm  = int(cfg["tempo_bpm"])
    key        = str(cfg["key"])
    scale_name = str(cfg["scale"])
    style      = str(cfg["style"])

    mf = MidiFile(ticks_per_beat=480)
    tempo = bpm2tempo(tempo_bpm)

    # Meta / tempo
    meta = MidiTrack(); mf.tracks.append(meta)
    meta.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    # Melody track
    mel = MidiTrack(); mf.tracks.append(mel)
    # Drums track (ch 9)
    drm = MidiTrack(); mf.tracks.append(drm)

    root = _key_root(key)
    pool = _scale_notes(root, scale_name)
    style_cfg = _style_params(style)

    # Basic structure: 4/4, 4 steps per beat = 16 steps per bar
    steps_per_bar = 16
    note_len_steps = 2  # eighths
    velocity = style_cfg["velocity"]

    # Melody: simple arpeggio-ish random walk per bar
    for b in range(bars):
        cur = random.choice(pool)
        for s in range(0, steps_per_bar, note_len_steps):
            nxt = random.choice(pool)
            # bias small moves
            if abs(nxt - cur) > 7:
                nxt = cur + random.choice([-5, -2, 2, 5])
            note = max(48, min(84, nxt))
            mel.append(Message('note_on', note=note, velocity=velocity, time=0))
            mel.append(Message('note_off', note=note, velocity=velocity, time=mf.ticks_per_beat//2))
            cur = note

    # Drums: simple pattern per bar
    kick_pat = style_cfg["kick_pat"]
    snr_pat  = style_cfg["snr_pat"]
    hat_den  = style_cfg["hat_density"]

    for b in range(bars):
        # 4 on the grid quarters for kick/snr decisions
        for q in range(4):
            # each quarter = 4 steps
            base_time = 4 * q * (mf.ticks_per_beat // 4)
            if kick_pat[q]:
                drm.append(Message('note_on', channel=9, note=DRUMS["kick"], velocity=100, time=0))
                drm.append(Message('note_off', channel=9, note=DRUMS["kick"], velocity=0, time=mf.ticks_per_beat//4))
            else:
                drm.append(Message('note_on', channel=9, note=0, velocity=0, time=mf.ticks_per_beat//4))  # just advance time

            if snr_pat[q]:
                drm.append(Message('note_on', channel=9, note=DRUMS["snare"], velocity=95, time=0))
                drm.append(Message('note_off', channel=9, note=DRUMS["snare"], velocity=0, time=mf.ticks_per_beat//4))
            else:
                drm.append(Message('note_on', channel=9, note=0, velocity=0, time=0))
                drm.append(Message('note_off', channel=9, note=0, velocity=0, time=0))

            # hats within the quarter
            hat_hits = max(1, hat_den)
            step = (mf.ticks_per_beat // 4) // hat_hits
            for h in range(hat_hits):
                drm.append(Message('note_on', channel=9, note=DRUMS["hat"], velocity=70, time=0))
                drm.append(Message('note_off', channel=9, note=DRUMS["hat"], velocity=0, time=step))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    mf.save(out_path)
    return out_path

def make_filename(params: Dict) -> Path:
    stamp = int(time.time())
    key = params.get("key","A"); sc = params.get("scale","minor"); sty = params.get("style","lofi"); bpm = params.get("tempo_bpm",84)
    name = f"{stamp}_{key}-{sc}_{sty}_{bpm}bpm.mid"
    return Path("outputs/beatmaker")/name
