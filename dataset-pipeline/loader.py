"""Load one recorded session: CSV samples plus JSON metadata."""
import json
from pathlib import Path
import pandas as pd

CHANNELS = ["ax", "ay", "az", "gx", "gy", "gz"]


def load_session(csv_path):
    csv_path = Path(csv_path)
    meta = json.loads(csv_path.with_suffix(".json").read_text())
    df = pd.read_csv(csv_path)
    return {
        "name": csv_path.stem,
        "label": meta["label"],
        "meta": meta,
        "t_ms": df["timestamp_ms"].to_numpy(),
        "X": df[CHANNELS].to_numpy().astype(float),
    }