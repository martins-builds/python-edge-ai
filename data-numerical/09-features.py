from pathlib import Path
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from scipy import signal

fs = 100.0
N = 250
win = signal.windows.hann(N, sym=False)
freqs = np.fft.rfftfreq(N, d=1/fs)

def features(w):
    w0 = w - w.mean()                                   # remove the offset
    mag = np.abs(np.fft.rfft(w0 * win)) * 2 / win.sum() # amplitude spectrum
    power = mag ** 2
    total = power.sum()
    zc = np.sum(np.signbit(w0[:-1]) != np.signbit(w0[1:]))   # sign changes
    return {
        "mean": w.mean(),
        "std": w.std(),
        "rms": np.sqrt(np.mean(w ** 2)),
        "p2p": w.max() - w.min(),
        "zcr_hz": zc / (len(w) / fs) / 2,
        "dom_freq": freqs[1:][np.argmax(mag[1:])] if total > 0 else 0.0,
        "centroid": (freqs * power).sum() / total if total > 0 else 0.0,
        "band_0_2": power[(freqs >= 0) & (freqs < 2)].sum(),
        "band_2_10": power[(freqs >= 2) & (freqs < 10)].sum(),
    }

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "embedded-tools" / "sensor-receiver" / "data" / "hw_test_20261107_090018.csv"
x = pd.read_csv(CSV)["ax"].to_numpy().astype(float)

hop = 125
windows = sliding_window_view(x, N)[::hop]
F = pd.DataFrame([features(w) for w in windows])
print(F.shape)
print(F.round(1).head(4))

quiet = np.full(250, 980.0)
shaky = 980 + 100 * np.sin(2 * np.pi * 7 * np.arange(250) / fs)
print({k: round(float(v), 1) for k, v in features(quiet).items()})
print({k: round(float(v), 1) for k, v in features(shaky).items()})

cols = ["ax", "ay", "az", "gx", "gy", "gz"]
X = pd.read_csv(CSV)[cols].to_numpy().astype(float)

rows = []
for start in range(0, len(X) - N + 1, hop):
    row = {"t_start_s": start / fs}
    for c, name in enumerate(cols):
        for k, v in features(X[start:start + N, c]).items():
            row[f"{name}_{k}"] = v
    rows.append(row)

F = pd.DataFrame(rows)
print(F.shape)