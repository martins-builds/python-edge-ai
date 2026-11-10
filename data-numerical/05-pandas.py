import pandas as pd

df = pd.read_csv("../embedded-tools/sensor-receiver/data/hw_test_20261107_090018.csv")

print(df.shape)         # (rows, columns)
print(list(df.columns)) # column names
print(df.dtypes)        # type of each column
print(df.head())        # first 5 rows
print(df.describe())    # count, mean, min, max for each column
gaps = df["timestamp_ms"].diff()           # time since the previous row (first is NaN)
print(gaps.value_counts())                 # expect: 10.0 for almost all rows
print("largest gap (ms):", gaps.max())

df["t"] = pd.to_timedelta(df["timestamp_ms"] - df["timestamp_ms"].iloc[0], unit="ms")
df = df.set_index("t")
print(df.index[:3])
# 1) one value per 100 ms (10 Hz): average the 10 samples in each bucket
slow = df["ax"].resample("100ms").mean()
print(len(df), "->", len(slow), "rows")
print(slow.head())

# 2) moving average over 5 samples, centred
smooth = df["ax"].rolling(5, center=True).mean()
print(smooth.head())
print("NaN count:", smooth.isna().sum())

# 3) back to NumPy
x = df["ax"].to_numpy()
print(type(x), x.shape)