import numpy as np

data = np.genfromtxt("/Users/macbookpro/Documents/GitHub/python-edge-ai/embedded-tools/sensor-receiver/data/test_20261023_155613.csv", delimiter=",", names=True)

print(data.dtype.names)          # column names from the header
ax = data["ax"]                  # one column as a 1-D array
print(ax.shape, ax.dtype)

print(ax[:5])                    # first 5 samples
print(ax[-5:])                   # last 5
print(ax.min(), ax.max(), ax.mean())

loud = ax[ax > 500]              # only samples above 500
print(len(loud), "samples above 500")

import numpy as np

data = np.genfromtxt("/Users/macbookpro/Documents/GitHub/python-edge-ai/embedded-tools/sensor-receiver/data/test_20261023_155613.csv", delimiter=",", names=True)
ax = data["ax"]
t = data["timestamp_ms"]

step = np.diff(ax)                       # change from each sample to the next
print("steps seen:", np.unique(np.round(step)))   # the distinct step sizes
print("big jumps:", (np.abs(step) > 100).sum())   # wraparounds / gaps

dt = np.diff(t)                          # time between samples, in ms
print("dt min/mean/max:", dt.min(), dt.mean(), dt.max())
print("gaps > 50 ms:", (dt > 50).sum())

centered = ax - ax.mean()                # remove the DC offset
print("mean after centering:", centered.mean())