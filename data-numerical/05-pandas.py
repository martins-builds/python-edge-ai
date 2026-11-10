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