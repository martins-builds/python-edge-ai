"""Split whole sessions (not windows) into train / val / test."""
import numpy as np


def assign_splits(label_by_session, seed=0, val_frac=0.2, test_frac=0.2):
    """Return {session: 'train' | 'val' | 'test'}, balanced per class."""
    by_label = {}
    for session, label in sorted(label_by_session.items()):
        by_label.setdefault(label, []).append(session)

    rng = np.random.default_rng(seed)
    out = {}
    for label, sessions in sorted(by_label.items()):
        if len(sessions) < 3:
            raise SystemExit(
                f"class '{label}' has {len(sessions)} session(s); "
                "need at least 3 (one each for train, val and test)")
        order = rng.permutation(len(sessions))
        n_test = max(1, round(test_frac * len(sessions)))
        n_val = max(1, round(val_frac * len(sessions)))
        for rank, idx in enumerate(order):
            if rank < n_test:
                out[sessions[idx]] = "test"
            elif rank < n_test + n_val:
                out[sessions[idx]] = "val"
            else:
                out[sessions[idx]] = "train"
    return out


def check_no_overlap(table):
    """Fail loudly if any session appears in more than one split."""
    sets = {s: set(table.loc[table["split"] == s, "session"])
            for s in ("train", "val", "test")}
    for a, b in (("train", "val"), ("train", "test"), ("val", "test")):
        shared = sets[a] & sets[b]
        if shared:
            raise AssertionError(f"sessions in both {a} and {b}: {sorted(shared)}")