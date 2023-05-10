# Import libraries and packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

companies = pd.read_csv("Unicorn_Companies.csv")

# Display the first 10 rows of the data
print(companies.head(10))

# Shape of the dataset
companies.shape

# Get information
companies.info()

# Get descriptive statistics
companies.describe()

# the to_datetime() function from the pandas library to converts the Date Joined column to datetime.
# This splits each value into year, month, and date components.
# This is an important step in data cleaning, as it makes the data in this column easier to use in tasks you may encounter
companies["Date Joined"] = pd.to_datetime(companies["Date Joined"])

# Use .info() to confirm that the update actually took place
companies.info()

# extract year component from 'Date Joined' column and Add the result as a new column named 'Year Joined' to the DataFrame

companies["Year Joined"] = companies["Date Joined"].dt.year

# Use .head() to confirm that the new column did get added
print(companies.head())

# Step 1: Use sample() with the n parameter set to 50 to randomly sample 50 unicorn companies from the data.
# Specify the random_state parameter so that if you run this cell multiple times, you get the same sample each time.
# Step 2: Save the result in a new variable.
companies_sample = companies.sample(n=50, random_state=42)

# Create bar plot
# with Industry column as the categories of the bars
# and the difference in years between Year Joined column and Year Founded column as the heights of the bars
plt.bar(
    companies_sample["Industry"],
    companies_sample["Year Joined"] - companies_sample["Year Founded"],
)

# Set title
plt.title(
    "Bar plot of maximum years taken by company to become unicorn per industry (from sample)"
)

# Set x-axis label
plt.xlabel("Industry")

# Set y-axis label
plt.ylabel("Maximum number of years")

# Rotate labels on the x-axis as a way to avoid overlap in the positions of the text
plt.xticks(rotation=45, horizontalalignment="right")

# Display the plot
plt.show()
