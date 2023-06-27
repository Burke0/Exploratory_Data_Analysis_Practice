import pandas as pd
import numpy as np
import seaborn as sns
import datetime
from matplotlib import pyplot as plt

import plotly.express as px  # Be sure to import express
# reduce size of db otherwise it could break

# read in first dataset
df=pd.read_csv('eda_missing_data_dataset1.csv')

# display first 10 rows
print(df.head(10))
print(df.shape)

# read in second dataset
df_zip=pd.read_csv('eda_missing_data_dataset2.csv')

#display first 10 rows
print(df_zip.head(10))
print(df_zip.shape)

# Left join the two datasets (all of the left and matching records)
# The dataframe you're calling the method on is always the left dataframe
df_joined = df.merge(df_zip, how='left', on=['date', 'center_point_geom'])

# print first 10 rows of merged data
print(df_joined.head(10))

# Get descriptive statistics of the joined dataframe
print(df_joined.describe())

# Create a new df of just the rows that are missing data
df_null_geo = df_joined[pd.isnull(df_joined.state_code)]
df_null_geo.shape

# Get non-null counts on merged dataframe
print(df_joined.info())

# Print the first 5 rows
print(df_null_geo.head())

# Create new df of just latitude, longitude, and number of strikes and group by latitude and longitude
top_missing = df_null_geo[['latitude','longitude','number_of_strikes_x']
            ].groupby(['latitude','longitude']
                      ).sum().sort_values('number_of_strikes_x',ascending=False).reset_index()

print(top_missing.head(10))

# create geographic scatter plot
fig = px.scatter_geo(top_missing[top_missing.number_of_strikes_x>=300],  # Input Pandas DataFrame
                    lat="latitude",  # DataFrame column with latitude
                    lon="longitude",  # DataFrame column with latitude
                    size="number_of_strikes_x") # Set to plot size as number of strikes
fig.update_layout(
    title_text = 'Lightning Data With No Address(Latitude and Longitude only)', # Create a Title
)

fig.show()

# plot scaled to United States only
fig = px.scatter_geo(top_missing[top_missing.number_of_strikes_x>=300],  # Input Pandas DataFrame
                    lat="latitude",  # DataFrame column with latitude
                    lon="longitude",  # DataFrame column with latitude
                    size="number_of_strikes_x") # Set to plot size as number of strikes
fig.update_layout(
    title_text = 'Lightning Data With No Address(Latitude and Longitude only)', # Create a Title
    geo_scope='usa',  # Plot only the USA instead of globe
)

fig.show()

# This explains why so many rows were missing state and zip code data! 
# Most of these lightning strikes occurred over water—the Atlantic Ocean, the Sea of Cortez, the Gulf of Mexico, the Caribbean Sea, and the Great Lakes. 
# Of the strikes that occurred over land, most of those were in Mexico, the Bahamas, and Cuba—places outside of the U.S. and without U.S. zip codes.
