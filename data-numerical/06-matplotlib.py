from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "embedded-tools" / "sensor-receiver" / "data" / "hw_test_20261107_090018.csv"

df = pd.read_csv(CSV)
fs = 100.0
t = (df["timestamp_ms"] - df["timestamp_ms"].iloc[0]).to_numpy() / 1000
x = df["ax"].to_numpy().astype(float)

cutoff = 1
sos = signal.butter(4, cutoff, btype="low", fs=fs, output="sos")
y = signal.sosfiltfilt(sos, x)

freqs = np.fft.rfftfreq(len(x), d=1/fs)
mag = np.abs(np.fft.rfft(x - x.mean())) * 2 / len(x)

fig, axs = plt.subplots(2, 1, figsize=(9, 6))

axs[0].plot(t, x, label="raw")
axs[0].plot(t, y, label=f"low-pass {cutoff} Hz")
axs[0].set_xlim(0, 6)
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("ax (counts)")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(freqs, mag)
axs[1].set_xlim(0, 20)
axs[1].set_xlabel("Frequency (Hz)")
axs[1].set_ylabel("Amplitude")
axs[1].set_title("Spectrum of ax")

fig.tight_layout()
fig.savefig(HERE / "ax_overview.png", dpi=120)
plt.show()

top = np.argsort(mag)[-4:][::-1]
print("strongest frequencies (Hz):", freqs[top].round(2))