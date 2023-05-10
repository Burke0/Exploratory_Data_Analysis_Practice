import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv_loader as h

# Read in the 2018 lightning strike dataset
df = h.load_csv()

# Inspect the first 10 rows
df.head(10)

df.shape

# Get more information about the data, including data types of each column
df.info()

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Calculate days with most lightning strikes
df.groupby(["date"]).sum().sort_values("number_of_strikes", ascending=False).head(10)

# Create a new `month` column
df["month"] = df["date"].dt.month
df.head()

# Calculate total number of strikes per month
# df.groupby(["month"]).sum().sort_values("number_of_strikes", ascending=False).head(12)
df.groupby(["month"])["number_of_strikes"].sum().sort_values(ascending=False).head(12)

# Create a new `month_txt` column
df["month_txt"] = df["date"].dt.month_name().str.slice(stop=3)
df.head()

# Create new helper dataframe for plotting
# df_by_month = (
#    df.groupby(["month", "month_txt"])
#    .sum()
#    .sort_values("month", ascending=True)
#    .head(12)
#    .reset_index()
# )
df_by_month = (
    df.groupby(["month", "month_txt"])["number_of_strikes"]
    .sum()
    .reset_index()
    .sort_values("month", ascending=True)
)

# Pyplot's plt.bar() function takes positional arguments of x and height, representing the data used for the x- and y- axes, respectively.
# We want the x-axis to represent months, and the y-axis to represent strike count.

plt.bar(
    x=df_by_month["month_txt"],
    height=df_by_month["number_of_strikes"],
    label="Number of strikes",
)
plt.plot()

plt.xlabel("Months(2018)")
plt.ylabel("Number of lightning strikes")
plt.title("Number of lightning strikes in 2018 by months")
plt.legend()
plt.show()
