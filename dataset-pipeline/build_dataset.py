"""Build a features table from recorded sessions.

    python build_dataset.py --raw raw --out dataset
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

from features import window_features
from loader import load_session, CHANNELS
from splits import assign_splits, check_no_overlap

META_COLS = ["session", "label", "t_start_s", "split"]


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
    ap.add_argument("--seed", type=int, default=0)
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

    # 1) split whole sessions, never single windows
    label_by_session = table.drop_duplicates("session").set_index("session")["label"].to_dict()
    split_of = assign_splits(label_by_session, seed=a.seed)
    table["split"] = table["session"].map(split_of)
    check_no_overlap(table)

    # 2) normalise with training statistics only
    feature_cols = [c for c in table.columns if c not in META_COLS]
    train = table[table["split"] == "train"]
    mean = train[feature_cols].mean()
    std = train[feature_cols].std(ddof=0).replace(0, 1.0)
    table[feature_cols] = (table[feature_cols] - mean) / std

    # 3) write outputs
    out = Path(a.out)
    out.mkdir(exist_ok=True)
    for name in ("train", "val", "test"):
        table[table["split"] == name].to_csv(out / f"{name}.csv", index=False)
    (out / "scaler.json").write_text(json.dumps(
        {"features": feature_cols, "mean": mean.tolist(), "std": std.tolist()}, indent=2))

    # 4) manifest: what was built, from what, with which settings
    h = hashlib.sha256()
    for p in csvs:
        for f in (p, p.with_suffix(".json")):
            h.update(f.read_bytes())
    config = {"fs": a.fs, "win": a.win, "hop": a.hop, "seed": a.seed}
    h.update(json.dumps(config, sort_keys=True).encode())
    manifest = {
        "dataset_id": h.hexdigest()[:12],
        "config": config,
        "channels": CHANNELS,
        "n_features": len(feature_cols),
        "splits": split_of,
        "windows": {s: table[table["split"] == s]["label"].value_counts().to_dict()
                    for s in ("train", "val", "test")},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print()
    print("dataset id:", manifest["dataset_id"])
    print("sessions per split:")
    print(pd.Series(split_of).value_counts().to_string())
    print("windows per split and class:")
    print(table.groupby(["split", "label"]).size().to_string())


if __name__ == "__main__":
    main()