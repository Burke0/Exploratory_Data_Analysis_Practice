import pandas as pd
import numpy as np
import seaborn as sns
import datetime
from matplotlib import pyplot as plt

# Read in 2016 data
df = pd.read_csv("eda_structuring_with_python_dataset1.csv")

print(df.head())

# Convert the 'date' column to datetime
df["date"] = pd.to_datetime(df["date"])

print(df.shape)

print(df.drop_duplicates().shape)

# Sort by number of strikes in descending order
print(df.sort_values(by="number_of_strikes", ascending=False).head(10))

# Identify locations that appear most in the dataset
print(df.center_point_geom.value_counts())

# Identify top 20 locations with the most days of lightning
print(
    df.center_point_geom.value_counts()[:20]
    .rename_axis("unique_values")
    .reset_index(name="counts")
)

# Lightning strikes by day of week
# Create two new columns
df["week"] = df.date.dt.isocalendar().week
df["weekday"] = df.date.dt.day_name()
print(df.head())

# Calculate mean count of lightning strikes for each weekday
print(df[["weekday", "number_of_strikes"]].groupby(["weekday"]).mean())

# Define order of days for the plot
weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# create boxplots of the strike counts for each day of the week

g = sns.boxplot(
    data=df, x="weekday", y="number_of_strikes", order=weekday_order, showfliers=False
)
g.set_title("Lightning distribution per weekday (2018)")
plt.show()

# Import 2016–2017 data
df_2 = pd.read_csv("eda_structuring_with_python_dataset2.csv")
print(df_2.head())

# Convert `date` column to datetime
df_2["date"] = pd.to_datetime(df_2["date"])

# Create new dataframe combining 2016–2017 data with 2018 data
union_df = pd.concat([df.drop(["weekday", "week"], axis=1), df_2], ignore_index=True)
print(union_df.head())

# add 3 new columns
union_df["year"] = union_df.date.dt.year
union_df["month"] = union_df.date.dt.month
union_df["month_txt"] = union_df.date.dt.month_name()
print(union_df.head())

# Calculate total number of strikes per year
union_df[["year", "number_of_strikes"]].groupby(["year"]).sum()

# Calculate total lightning strikes for each month of each year
lightning_by_month = (
    union_df.groupby(["month_txt", "year"])
    .agg(number_of_strikes=pd.NamedAgg(column="number_of_strikes", aggfunc=sum))
    .reset_index()
)

print(lightning_by_month.head())

# Calculate total lightning strikes for each year
lightning_by_year = (
    union_df.groupby(["year"])
    .agg(year_strikes=pd.NamedAgg(column="number_of_strikes", aggfunc=sum))
    .reset_index()
)

lightning_by_year.head()

# Combine `lightning_by_month` and `lightning_by_year` dataframes into single dataframe
percentage_lightning = lightning_by_month.merge(lightning_by_year, on="year")
percentage_lightning.head()

# Create new `percentage_lightning_per_month` column
percentage_lightning["percentage_lightning_per_month"] = (
    percentage_lightning.number_of_strikes / percentage_lightning.year_strikes * 100.0
)
percentage_lightning.head()

plt.figure(figsize=(10, 6))

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# plot percentage lightning per month
sns.barplot(
    data=percentage_lightning,
    x="month_txt",
    y="percentage_lightning_per_month",
    hue="year",
    order=month_order,
)
plt.xlabel("Month")
plt.ylabel("% of lightning strikes")
plt.title("% of lightning strikes each Month (2016-2018)")
plt.show()
