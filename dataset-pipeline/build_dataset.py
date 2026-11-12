"""Build a features table from recorded sessions.

    python build_dataset.py --raw raw --out dataset
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from features import window_features
from loader import load_session, CHANNELS


def windows_for_session(s, win, hop):
    """Yield (start_index, window) pairs. Windows never span a time gap."""
    X, t = s["X"], s["t_ms"]
    if len(X) < win:
        return
    step = np.median(np.diff(t))
    gap_at = np.where(np.diff(t) > 1.5 * step)[0]          # gap after sample i
    W = np.moveaxis(sliding_window_view(X, win, axis=0), 2, 1)
    for start in range(0, len(W), hop):
        if np.any((gap_at >= start) & (gap_at < start + win - 1)):
            continue
        yield start, W[start]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="raw")
    ap.add_argument("--out", default="dataset")
    ap.add_argument("--fs", type=float, default=100.0)
    ap.add_argument("--win", type=int, default=250)
    ap.add_argument("--hop", type=int, default=125)
    a = ap.parse_args()

    csvs = sorted(Path(a.raw).glob("*.csv"))
    if not csvs:
        raise SystemExit(f"no CSV files in {a.raw}")

    rows = []
    for path in csvs:
        s = load_session(path)
        n_before = len(rows)
        for start, w in windows_for_session(s, a.win, a.hop):
            row = {"session": s["name"], "label": s["label"],
                   "t_start_s": start / a.fs}
            row.update(window_features(w, a.fs, CHANNELS))
            rows.append(row)
        print(f"{s['name']:28s} {s['label']:10s} {len(rows) - n_before:3d} windows")

    table = pd.DataFrame(rows)
    out = Path(a.out)
    out.mkdir(exist_ok=True)
    table.to_csv(out / "features.csv", index=False)
    print()
    print("windows per class:")
    print(table["label"].value_counts().to_string())
    print("table shape:", table.shape)


if __name__ == "__main__":
    main()