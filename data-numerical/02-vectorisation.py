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