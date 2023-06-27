#############################
##### Step 1: Imports #######
#############################

# Import libraries and modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Read the data into a dataframe
df_companies = pd.read_csv('Unicorn_Companies.csv')

######################################
###### Step 2: Data exploration ######
######################################

# Display the first 10 rows of the data.
print(df_companies.head(10))

# Get the shape of the dataset.
print(df_companies.shape)

# Get the data types and number of non-null values in the dataset.
print(df_companies.info())

# Get descriptive statistics such as mean, standard deviation, and range of the numerical columns in the dataset.
print(df_companies.describe())

# The oldest company in the list was founded in 1919. This is the minimum value in Year Funded using the describe() method. 

# Create a new column `Year Joined` 
df_companies['Year_Joined'] = pd.to_datetime(df_companies['Date Joined']).dt.year

# Define the `str_to_num()` function to convert valuation column to numeric data type
def str_to_num(x):
    x = x.strip('$B')
    x = int(x)

    return x

# Apply the `str_to_num()` function to the `Valuation` column
# and assign the result back to a new column called `valuation_num`

df_companies['valuation_num'] = df_companies['Valuation'].apply(str_to_num)
print(df_companies[['Valuation', 'valuation_num']].head())

# Find the number of missing values in each column in this dataset.
print(df_companies.isna().sum())

# 1. Apply the `isna()` method to the `df_companies` dataframe and assign back to `mask`
# each value is True if its contents are NaN and a False if its contents are not NaN
mask = df_companies.isna()
print(mask.tail())

# This means that you need a way to find the indices of the rows of the Boolean dataframe that contain at least one True value, 
# then extract those indices from df_companies. 
# You can do this using the any() method for DataFrame objects. 
# This method returns a Boolean Series indicating whether any value is True over a specified axis.

# 2. Apply the `any()` method to `mask` and assign the results back to `mask`
mask = mask.any(axis=1)
print(mask.head())

# 3. Apply `mask` as a Boolean mask to `df_companies` and assign results to `df_missing_rows` 
# to return a filtered dataframe containing just the rows that contain a missing value
df_missing_rows = df_companies[mask]
print(df_missing_rows)

# Twelve of the 17 rows with missing values are for companies from Singapore.

#####################################
###### Step 3: Model building #######
#####################################

# There are several ways to address missing values, which is critical in EDA. 
# The two primary methods are removing them and imputing other values in their place

##### Method 1: removal ######

# Store the total number of values in a variable called `count_total`
count_total = df_companies.size
print(count_total)

# Drop the rows containing missing values, determine number of remaining values 
count_dropna_rows = df_companies.dropna().size
print(count_dropna_rows)

# Drop the columns containing missing values, determine number of remaining values
count_dropna_columns = df_companies.dropna(axis=1).size
print(count_dropna_columns)

# Print the percentage of values removed by dropping rows.
row_percent = (count_total - count_dropna_rows) / count_total
print(f'Percentage removed, rows: {row_percent:.3f}')

# Print the percentage of values removed by dropping columns.
col_percent = (count_total - count_dropna_columns) / count_total
print(f'Percentage removed, columns: {col_percent:.3f}')

# The percentage removed was significantly higher for columns than it was for rows. 
# Since both approaches result in a dataset with no missing values, 
# the "most effective" method depends on how much data you have and what you want to do with it

##### Method 2: imputation #####

# 1. Fill missing values using the 'fillna()' method, back-filling(fill each missing value with the next non-NaN value in its column.)
df_companies_backfill = df_companies.fillna(method='backfill')

# 2. Show the rows that previously had missing values
df_companies_backfill.iloc[df_missing_rows.index, :]

# This method does not work well with this dataset since the values are added without consideration for which country those cities are located in
# Another option is to fill values with a certain value as 'unknown' but that isn't useful here because it doesnt add value to the data set and can make it harder to find those rows.

###############################################
######## Step 4: Results and evaluation #######
###############################################

# Task 1: Find companies in the Hardware industry in the following cities: Beijing, San Francisco, and London.
# Task 2: Find companies in the Artificial intelligence industry in London. 

# 1. Create a Boolean mask using conditional logic
cities = ['Beijing', 'San Francisco', 'London']
mask = (
    (df_companies['Industry']=='Hardware') & (df_companies['City'].isin(cities))
) | (
    (df_companies['Industry']=='Artificial intelligence') & (df_companies['City']=='London')
)

# 2. Apply the mask to the `df_companies` dataframe and assign the results to `df_invest`
df_invest = df_companies[mask]
print(df_invest)
# Eight companies meet this criteria!

# Task 3: List of countries by sum of valuation and ignore outliers(United States, China, India, and the United Kingdom)

# Group the data by`Country/Region`
national_valuations = df_companies.groupby(['Country/Region'])['valuation_num'].sum(
).sort_values(ascending=False).reset_index()

# Print the top 15 values of the DataFrame
print(national_valuations.head(15))

# Filter out top 4 outlying countries
national_valuations_no_big4 = national_valuations.iloc[4:, :]

print(national_valuations_no_big4.head())

# Alternative approach
# Use `isin()` to create a Boolean mask to accomplish the same task
# mask = ~national_valuations['Country/Region'].isin(['United States', 'China', 'India', 'United Kingdom'])
# national_valuations_no_big4 = national_valuations[mask]
# national_valuations_no_big4.head()

# Create a barplot to compare the top 20 non-big-4 countries with highest company valuations
sns.barplot(data=national_valuations_no_big4.head(20),
            y='Country/Region',
            x='valuation_num')
plt.title('Top 20 non-big-4 countries by total company valuation')
plt.show()

# Plot the sum of valuations per country. Valuation sum per country is visualized by the size of circles around the map.
data = national_valuations_no_big4

fig = px.scatter_geo(data, 
                     locations='Country/Region', 
                     size='valuation_num', 
                     locationmode='country names', 
                     color='Country/Region',
                     title='Total company valuations by country (non-big-four)')
fig.show()
