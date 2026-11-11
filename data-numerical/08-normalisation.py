from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "embedded-tools" / "sensor-receiver" / "data" / "hw_test_20261107_090018.csv"
df = pd.read_csv(CSV)

cols = ["ax", "ay", "az", "gx", "gy", "gz"]
X = df[cols].to_numpy().astype(float)

mean, std = X.mean(axis=0), X.std(axis=0)
print("mean:", mean.round(2))
print("std: ", std.round(2))

with np.errstate(divide="ignore", invalid="ignore"):
    bad = (X - mean) / std
print("NaN per column (unsafe):", np.isnan(bad).sum(axis=0))

std_safe = np.where(std == 0, 1.0, std)
Z = (X - mean) / std_safe
print("z-score mean:", Z.mean(axis=0).round(3))
print("z-score std: ", Z.std(axis=0).round(3))

split = int(0.7 * len(X))
m_tr = X[:split].mean(axis=0)
s_tr = X[:split].std(axis=0)
s_tr = np.where(s_tr == 0, 1.0, s_tr)
Z_test = (X[split:] - m_tr) / s_tr
print("test ax mean/std:", Z_test[:, 0].mean().round(3), Z_test[:, 0].std().round(3))

np.savez(HERE / "scaler.npz", mean=m_tr, std=s_tr)