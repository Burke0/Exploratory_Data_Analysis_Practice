import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in the data.
df = pd.read_csv("eda_manipulate_date_strings_with_python.csv")
print(df.head())

# Convert the `date` column to datetime.
df["date"] = pd.to_datetime(df["date"])

# Create four new columns.
df["week"] = df["date"].dt.strftime("%Y-W%V")
df["month"] = df["date"].dt.strftime("%Y-%m")
df["quarter"] = df["date"].dt.to_period("Q").dt.strftime("%Y-Q%q")
df["year"] = df["date"].dt.strftime("%Y")

print(df.head(10))

# Create a new dataframe view of just 2018 data, summed by week.
df_by_week_2018 = (
    df[df["year"] == "2018"].groupby(["week"]).sum(numeric_only=True).reset_index()
)
print(df_by_week_2018.head())

# Plot a bar graph of weekly strike totals in 2018.
plt.figure(figsize=(20, 5))  # Increase output size
plt.bar(x=df_by_week_2018["week"], height=df_by_week_2018["number_of_strikes"])
plt.plot()
plt.xlabel("Week number")
plt.ylabel("Number of lightning strikes")
plt.title("Number of lightning strikes per week (2018)")
plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels and decrease font size

plt.show()

# plot the number of quarterly lightening strikes from 2016-2018

# Group 2016-2018 data by quarter and sum
df_by_quarter = df.groupby(["quarter"]).sum(numeric_only=True).reset_index()

# Format as text, in millions
df_by_quarter["number_of_strikes_formatted"] = (
    df_by_quarter["number_of_strikes"].div(1000000).round(1).astype(str) + "M"
)

print(df_by_quarter.head())


# Iterates over data and plots text labels above each bar of the bar graph
def addLabels(x, y, labels):
    for i in range(len(x)):
        plt.text(i, y[i], labels[i], ha="center", va="bottom")


plt.figure(figsize=(15, 5))
plt.bar(x=df_by_quarter["quarter"], height=df_by_quarter["number_of_strikes"])
addLabels(
    df_by_quarter["quarter"],
    df_by_quarter["number_of_strikes"],
    df_by_quarter["number_of_strikes_formatted"],
)
plt.plot()
plt.xlabel("Quarter")
plt.ylabel("Number of lightning strikes")
plt.title("Number of lightning strikes per quarter (2016-2018)")
plt.show()

# create a grouped bar chart to better compare year-over-year changes each quarter.

# First, create two new columns
df_by_quarter["quarter_number"] = df_by_quarter["quarter"].str[-2:]
df_by_quarter["year"] = df_by_quarter["quarter"].str[:4]
print(df_by_quarter.head())


# Create a bar plot using Seaborn library
plt.figure(figsize=(15, 5))
p = sns.barplot(
    data=df_by_quarter, x="quarter_number", y="number_of_strikes", hue="year"
)

# Annotate each bar with its height (number of lightning strikes in millions)
for b in p.patches:
    p.annotate(
        str(round(b.get_height() / 1000000, 1)) + "M",
        (b.get_x() + b.get_width() / 2.0, b.get_height() + 1.2e6),
        ha="center",
        va="bottom",
        xytext=(0, -12),
        textcoords="offset points",
    )
# Set the labels and titles for the plot
plt.xlabel("Quarter")
plt.ylabel("Number of lightning strikes")
plt.title("Number of lightning strikes per quarter (2016-2018)")
plt.show()
