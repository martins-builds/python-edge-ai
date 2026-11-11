from pathlib import Path
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from scipy import signal

fs = 100.0

# testing leakage, with and without a Hann window
t = np.arange(0, 10, 1/fs)
s = np.sin(2*np.pi*0.55*t)                  # does NOT fit a whole number of cycles in 10 s
N = len(s)
f = np.fft.rfftfreq(N, d=1/fs)

rect = np.ones(N)
hann = signal.windows.hann(N, sym=False)

def spec(sig, win):
    return np.abs(np.fft.rfft(sig * win)) * 2 / win.sum()

a = spec(s, rect)
b = spec(s, hann)
print("rectangular: peak", f[a.argmax()], "Hz, amplitude", a.max().round(3))
print("hann:        peak", f[b.argmax()], "Hz, amplitude", b.max().round(3))

def db_at(spectrum, freq):
    i = np.argmin(abs(f - freq))
    return (20*np.log10(spectrum[i] / spectrum.max())).round(1)

print("leakage at 3 Hz (dB):  rect", db_at(a, 3), " hann", db_at(b, 3))
print("leakage at 10 Hz (dB): rect", db_at(a, 10), " hann", db_at(b, 10))

#windows from my recording
HERE = Path(__file__).resolve().parent #easier thn os path
CSV = HERE.parent / "embedded-tools" / "sensor-receiver" / "data" / "hw_test_20261107_090018.csv"
x = pd.read_csv(CSV)["ax"].to_numpy().astype(float)

Nw, hop = 250, 125
windows = sliding_window_view(x, Nw)[::hop]
print("windows:", windows.shape, "expected", (len(x) - Nw) // hop + 1)
print("window start times (s):", (np.arange(len(windows)) * hop / fs)[:4])