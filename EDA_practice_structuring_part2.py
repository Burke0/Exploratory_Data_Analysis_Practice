import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset provided into a DataFrame.
companies = pd.read_csv("Unicorn_Companies.csv")

# Display the first 10 rows of the data.
print(companies.head(10))

# Identify the number of rows and columns in the dataset.
print(companies.shape)

# Check for duplicates.
print(companies.drop_duplicates().shape)

# Display the data types of the columns.
print(companies.dtypes)

# Sort `companies` and display the first 10 rows of the resulting DataFrame.
# and arrange the data from latest to earliest `Year Founded`
print(companies.sort_values(by="Year Founded", ascending=False).head(10))

# Display each unique year that occurs in the dataset
# along with the number of companies that were founded in each unique year.
print(companies["Year Founded"].value_counts().sort_values(ascending=False))

# Convert `Date Joined` column to datetime.
# Update the column with the converted values
companies["Date Joined"] = pd.to_datetime(companies["Date Joined"])

# Display the data types of the columns in `companies`
# to confirm that the update actually took place
print(companies.dtypes)

# Obtain the names of the months when companies gained unicorn status.
# Use the result to create a `Month Joined` column.

companies["Month Joined"] = companies["Date Joined"].dt.month_name()

# Display the first few rows of `companies`
# to confirm that the new column did get added.
print(companies.head())

# Determine how many years it took for companies to reach unicorn status.
# Use the result to create a `Years To Join` column.
companies["Years To Join"] = (
    companies["Date Joined"].dt.year - companies["Year Founded"]
)

# Display the first few rows of `companies`
# to confirm that the new column did get added.
print(companies.head())

# Filter dataset by a year of your interest (in terms of when companies reached unicorn status).
# Save the resulting subset in a new variable .
companies_2021 = companies[companies["Date Joined"].dt.year == 2021]

# Display the first few rows of the subset to confirm that it was created
print(companies_2021.head())

# After identifying the time interval that interests you, proceed with the following:
# Step 1. Take the subset that you defined for the year of interest.
#         Insert a column that contains the time interval that each data point belongs to, as needed.
# Step 2. Group by the time interval.
#         Aggregate by counting companies that joined per interval of that year.
#         Save the resulting DataFrame in a new variable.

# Insert a `Week Joined` column into `companies_2021.`
companies_2021.insert(
    3, "Week Joined", companies_2021["Date Joined"].dt.strftime("%Y-W%V"), True
)

# Group `companies_2021` by `Week Joined`.
# Aggregate by counting companies that joined per week of 2021.
# Save the resulting DataFrame in a new variable.
companies_by_week_2021 = (
    companies_2021.groupby(by="Week Joined")["Company"]
    .count()
    .reset_index()
    .rename(columns={"Company": "Company Count"})
)

# Display the first few rows of the new DataFrame to confirm that it was created.

print(companies_by_week_2021.head())


# After identifying the additional year and time interval of interest, proceed with the following:
# Step 1. Filter by the additional year to create a subset that consists of companies that joined in that year.
# Step 2. Concatenate that new subset with the subset that you defined previously.
# Step 3. As needed, add a column that contains the time interval that each data point belongs to,
#         in the concatenated DataFrame.
# Step 4. Transform the `Valuation` column as needed.
# Step 5. Group by the time interval.
#         Aggregate by computing average funding of companies that joined per interval of the corresponding year.
#         Save the resulting DataFrame in a new variable.

# Filter by the additional year to create a subset that consists of companies that joined in that year.
companies_2020 = companies[companies["Date Joined"].dt.year == 2020]

# Concatenate the new subset with the subset that you defined previously.
companies_2020_2021 = pd.concat(
    [companies_2020, companies_2021.drop(columns="Week Joined")]
)

# Add `Quarter Joined` column to `companies_2021`.
companies_2020_2021["Quarter Joined"] = (
    companies_2020_2021["Date Joined"].dt.to_period("Q").dt.strftime("%Y-Q%q")
)

# Convert the `Valuation` column to numeric by removing `$` and `B` and casting each value to data type `float`.
companies_2020_2021["Valuation"] = (
    companies_2020_2021["Valuation"].apply(lambda v: v.strip("$B")).astype(float)
)

# Group `companies_2020_2021` by `Quarter Joined`,
# Aggregate by computing average `Funding` of companies that joined per quarter of each year.
# Save the resulting DataFrame in a new variable.
companies_by_quarter_2020_2021 = (
    companies_2020_2021.groupby(by="Quarter Joined")["Valuation"]
    .mean()
    .reset_index()
    .rename(columns={"Valuation": "Average Valuation"})
)

# Display the first few rows of the new DataFrame to confirm that it was created.

print(companies_by_quarter_2020_2021.head())


########################################################################
##### Visualize the time it took companies to become unicorns ##########
########################################################################

# Define a list that contains months in chronological order.
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

# Create the box plot
# to visualize the distribution of how long it took companies to become unicorns,
# with respect to the month they joined.
# Make sure the x-axis goes in chronological order by month, using the list you defined previously.
# Plot the data from the `companies` DataFrame.

sns.boxplot(
    x=companies["Month Joined"],
    y=companies["Years To Join"],
    order=month_order,
    showfliers=False,
)

# Set the title of the plot.
plt.title("Distribution of years to become unicorn with respect to month joined")

# Rotate labels on the x-axis as a way to avoid overlap in the positions of the text.
plt.xticks(rotation=45, horizontalalignment="right")

# Display the plot.
plt.show()

#########################################################################
##### Visualize the time it took companies to reach unicorn status ######
#########################################################################

# Set the size of the plot.
plt.figure(figsize=(10, 6))

# Create bar plot to visualize the average number of years it took companies to reach unicorn status
# with respect to when they were founded.
# Plot data from the `companies` DataFrame.
sns.barplot(x=companies["Year Founded"], y=companies["Years To Join"], ci=False)

# Set title
plt.title("Bar plot of years to join with respect to year founded")

# Set x-axis label
plt.xlabel("Year founded")

# Set y-axis label
plt.ylabel("Years to join unicorn status")

# Rotate the labels on the x-axis as a way to avoid overlap in the positions of the text.
plt.xticks(rotation=45, horizontalalignment="right")

# Display the plot.
plt.show()

########################################################################
##### Visualize the number of companies that joined per interval #######
########################################################################

# Set the size of the plot.
plt.figure(figsize=(20, 5))

# Create bar plot to visualize number of companies that joined per interval for the year of interest.
plt.bar(
    x=companies_by_week_2021["Week Joined"],
    height=companies_by_week_2021["Company Count"],
)
plt.plot()

# Set the x-axis label.
plt.xlabel("Week number")

# Set the y-axis label.
plt.ylabel("Number of companies")

# Set the title.
plt.title("Number of companies that became unicorns per week in 2021")

# Rotate the labels on the x-axis as a way to avoid overlap in the positions of the text.
plt.xticks(rotation=45, horizontalalignment="right", fontsize=8)

# Display the plot.
plt.show()

############################################################
#### Visualize the average valuation over the quarters #####
############################################################

# Using slicing, extract the year component and the time interval that you specified,
# and save them by adding two new columns into the subset.

companies_by_quarter_2020_2021["Quarter Number"] = companies_by_quarter_2020_2021[
    "Quarter Joined"
].str[-2:]
companies_by_quarter_2020_2021["Year Joined"] = companies_by_quarter_2020_2021[
    "Quarter Joined"
].str[:4]

# Set the size of the plot.
plt.figure(figsize=(10, 5))

# Create a grouped bar plot.
sns.barplot(
    x=companies_by_quarter_2020_2021["Quarter Number"],
    y=companies_by_quarter_2020_2021["Average Valuation"],
    hue=companies_by_quarter_2020_2021["Year Joined"],
)
plt.plot()

# Set the x-axis label.
plt.xlabel("Quarter number")

# Set the y-axis label.
plt.ylabel("Average valuation (billions of dollars)")

# Set the title.
plt.title(
    "Average valuation of companies that became unicorns per quarter in 2020 vs. 2021"
)

# Display the plot.
plt.show()
