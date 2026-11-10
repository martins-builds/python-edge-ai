import pandas as pd

df = pd.read_csv("../embedded-tools/sensor-receiver/data/hw_test_20261107_090018.csv")

print(df.shape)         # (rows, columns)
print(list(df.columns)) # column names
print(df.dtypes)        # type of each column
print(df.head())        # first 5 rows
print(df.describe())    # count, mean, min, max for each column