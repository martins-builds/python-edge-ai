import numpy as np
import matplotlib.pyplot as plt

fs = 100.0
t = np.arange(0, 10, 1/fs)
x = 999*np.sin(2*np.pi*0.5*t) + 300*np.sin(2*np.pi*5*t) + 50

X = np.fft.rfft(x - x.mean())
freqs = np.fft.rfftfreq(len(x), d=1/fs)
mag = np.abs(X) * 2 / len(x)

top = np.argsort(mag)[-2:][::-1]
print(freqs[top], mag[top])        # [0.5 5.] [999. 300.]

plt.plot(freqs, mag)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.show()