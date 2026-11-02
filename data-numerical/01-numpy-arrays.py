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