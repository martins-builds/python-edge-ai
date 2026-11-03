import numpy as np
import matplotlib.pyplot as plt

def spectrum(x, fs):
    x = x - x.mean()
    freqs = np.fft.rfftfreq(len(x), d=1/fs)
    mag = np.abs(np.fft.rfft(x)) * 2 / len(x)
    return freqs, mag

fs = 100.0

# 1) synthetic signal, to see that the method works
t = np.arange(0, 10, 1/fs)
fake = 999*np.sin(2*np.pi*0.5*t) + 300*np.sin(2*np.pi*5*t) + 50
f1, m1 = spectrum(fake, fs)
print("synthetic peaks:", f1[np.argsort(m1)[-2:][::-1]])

# 2) your real recording
data = np.genfromtxt("embedded-tools/sensor-receiver/data/test_20261023_155613.csv", delimiter=",", names=True)
f2, m2 = spectrum(data["ax"], fs)
print("recording peak:", f2[np.argmax(m2)], "Hz, amplitude", m2.max())

f3, m3 = spectrum(data["ax"][:1000], fs)   # only the first 10 seconds
plt.plot(f2, m2, label="full recording")
plt.plot(f3, m3, label="first 1000 samples")
plt.xlim(0, 3)                              # zoom in near the peak
plt.legend()
plt.show()