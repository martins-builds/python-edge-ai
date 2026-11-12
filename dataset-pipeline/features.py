"""Window features for IMU data: nine features per channel."""
import numpy as np
from scipy import signal

FEATURE_NAMES = ["mean", "std", "rms", "p2p", "zcr_hz",
                 "dom_freq", "centroid", "band_0_2", "band_2_10"]


def channel_features(w, fs, win, freqs):
    """Nine features for one channel of one window (1-D array)."""
    w0 = w - w.mean()
    mag = np.abs(np.fft.rfft(w0 * win)) * 2 / win.sum()
    power = mag ** 2
    total = power.sum()
    zc = np.sum(np.signbit(w0[:-1]) != np.signbit(w0[1:]))
    values = [
        w.mean(),
        w.std(),
        np.sqrt(np.mean(w ** 2)),
        w.max() - w.min(),
        zc / (len(w) / fs) / 2,
        freqs[1:][np.argmax(mag[1:])] if total > 0 else 0.0,
        (freqs * power).sum() / total if total > 0 else 0.0,
        power[(freqs >= 0) & (freqs < 2)].sum(),
        power[(freqs >= 2) & (freqs < 10)].sum(),
    ]
    return dict(zip(FEATURE_NAMES, values))


def window_features(window, fs, channel_names):
    """Features for a window of shape (N, channels). Returns a flat dict."""
    n = window.shape[0]
    win = signal.windows.hann(n, sym=False)
    freqs = np.fft.rfftfreq(n, d=1 / fs)
    row = {}
    for c, name in enumerate(channel_names):
        feats = channel_features(window[:, c], fs, win, freqs)
        for k, v in feats.items():
            row[f"{name}_{k}"] = float(v)
    return row