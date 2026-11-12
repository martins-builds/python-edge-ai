"""Create synthetic sessions (3 classes x 3 sessions) to test the pipeline.

These are NOT real data. They live in raw_fake/, never in raw/.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

FS = 100
SECONDS = 60
OUT = Path("raw_fake")
OUT.mkdir(exist_ok=True)
CHANNELS = ["ax", "ay", "az", "gx", "gy", "gz"]


def make(label, rng):
    n = FS * SECONDS
    t = np.arange(n) / FS
    ph = rng.uniform(0, 2 * np.pi)
    X = rng.normal(0, 5, (n, 6))
    X[:, 2] += 980
    if label == "walking":
        f = rng.uniform(1.6, 2.2)
        X[:, 2] += 250 * np.sin(2 * np.pi * f * t + ph)
        X[:, 0] += 150 * np.sin(2 * np.pi * f * t + ph + 1)
        X[:, 3] += 40 * np.sin(2 * np.pi * f * t + ph)
    elif label == "jumping":
        period = rng.uniform(1.0, 1.4)
        phase = (t % period) / period
        X[:, 2] += 1500 * np.exp(-12 * phase) * (phase < 0.5)
        X[:, 3] += 100 * np.exp(-8 * phase)
    return np.round(X).astype(int)


rng = np.random.default_rng(42)
for label in ["sitting", "walking", "jumping"]:
    for k in range(3):
        X = make(label, rng)
        stamp = f"20261112_1{len(list(OUT.glob('*.csv'))):02d}000"
        name = f"{label}_{stamp}"
        df = pd.DataFrame(X, columns=CHANNELS)
        df.insert(0, "timestamp_ms", 5000 + np.arange(len(X)) * 10)
        df.to_csv(OUT / f"{name}.csv", index=False)
        meta = {"label": label, "samples": len(X), "measured_rate_hz": 100.0,
                "synthetic": True, "csv": f"{name}.csv"}
        (OUT / f"{name}.json").write_text(json.dumps(meta, indent=2))
        print("wrote", name)