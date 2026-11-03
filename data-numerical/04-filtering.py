import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def spectrum(x, fs):
    x = x - x.mean()
    freqs = np.fft.rfftfreq(len(x), d=1/fs)
    mag = np.abs(np.fft.rfft(x)) * 2 / len(x)
    return freqs, mag

fs = 100.0
t = np.arange(0, 10, 1/fs)
clean = 999 * np.sin(2*np.pi*0.5*t)

rng = np.random.default_rng(0)
noisy = clean + 150*np.sin(2*np.pi*20*t) + rng.normal(0, 50, len(t))

sos = signal.butter(4, 3, btype="low", fs=fs, output="sos")
offline = signal.sosfiltfilt(sos, noisy)
live = signal.sosfilt(sos, noisy)

def rms_error(a, b):
    return np.sqrt(np.mean((a - b)**2))

print("noisy   error:", rms_error(noisy, clean).round(1))
print("offline error:", rms_error(offline, clean).round(1))
print("live    error:", rms_error(live, clean).round(1))

plt.plot(t, noisy, alpha=0.4, label="noisy")
plt.plot(t, offline, label="sosfiltfilt (no delay)")
plt.plot(t, live, label="sosfilt (delayed)")
plt.plot(t, clean, "k--", label="true signal")
plt.legend()
plt.show()

f, m = spectrum(noisy, fs)
top = np.argsort(m)[-2:][::-1]
print(f[top], m[top].round(0))

plt.plot(f, m)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.show()