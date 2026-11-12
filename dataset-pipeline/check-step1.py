import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from features import window_features
from loader import load_session, CHANNELS

s = load_session("raw/hw_test_20261107_090018.csv")
print(s["name"], s["label"], s["X"].shape)

W = sliding_window_view(s["X"], 250, axis=0)   # (windows, channels, 250)
W = np.moveaxis(W, 2, 1)[::125]                # -> (windows, 250, channels), 50% overlap
print(W.shape)

row = window_features(W[0], 100.0, CHANNELS)
print(len(row), "features in one row")
print({k: round(row[k], 1) for k in ["ax_mean", "ax_std", "ax_dom_freq", "az_mean", "ay_std"]})