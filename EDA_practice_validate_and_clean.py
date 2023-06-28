#######################################
######## Step 1: Imports ##############
#######################################
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Run this cell so pandas displays all columns
pd.set_option('display.max_columns', None)

# Import data
companies = pd.read_csv('Modified_Unicorn_Companies.csv')

# Display first 10 rows
print(companies.head(10))

########################################
####### Step 2: Data cleaning ##########
########################################

# Display data types of columns
print(companies.dtypes)

# Convert 'Date Joined' to datetime
companies['Date Joined'] = pd.to_datetime(companies['Date Joined'])

# Create the column Years To Unicorn.
companies['Years To Unicorn'] = companies['Date Joined'].dt.year - companies['Year Founded']

###### Input validation ######

# Identify and correct the issue with Years To Unicorn.
print(companies['Years To Unicorn'].describe())

# There seems to be a negative value!
# Isolate any rows where `Years To Unicorn` is negative
print(companies[companies['Years To Unicorn'] < 0])

# It seems the date InVisionwas founded is incorrect and should be 2011 instead
# Replace InVision's `Year Founded` value with 2011
companies.loc[companies['Company'] == 'InVision', 'Year Founded'] = 2011

# Verify the change was made properly
print(companies[companies['Company'] == 'InVision'])

# Recalculate all values in the `Years To Unicorn` column
companies['Years To Unicorn'] = companies['Date Joined'].dt.year - companies['Year Founded']

# Verify that there are no more negative values in the column
print(companies['Years To Unicorn'].describe())

# List provided by the company of the expected industry labels in the data
industry_list = ['Artificial intelligence', 'Other','E-commerce & direct-to-consumer', 'Fintech',\
       'Internet software & services','Supply chain, logistics, & delivery', 'Consumer & retail',\
       'Data management & analytics', 'Edtech', 'Health', 'Hardware','Auto & transportation', \
        'Travel', 'Cybersecurity','Mobile & telecommunications']

# Check which values are in `Industry` but not in `industry_list`
print(set(companies['Industry']) - set(industry_list))

# It seems there were a few misspellings of some of the labels

# 1. Create `replacement_dict`
replacement_dict = {'Artificial Intelligence': 'Artificial intelligence',
                   'Data management and analytics': 'Data management & analytics',
                   'FinTech': 'Fintech'
                   }

# 2. Replace the incorrect values in the `Industry` column
companies['Industry'] = companies['Industry'].replace(replacement_dict)

# 3. Verify that there are no longer any elements in `Industry` that are not in `industry_list`
print(set(companies['Industry']) - set(industry_list))

# Isolate rows of all companies that have duplicates
print(companies[companies.duplicated(subset=['Company'], keep=False)])

# Drop rows of duplicate companies after their first occurrence
companies = companies.drop_duplicates(subset=['Company'], keep='first')

####### Convert categorical data to numerical data ##########

# Rank the continents by number of unicorn companies
companies['Continent'].value_counts()

# Create numeric `Continent Number` column
continent_dict = {'North America': 1,
                  'Asia': 2,
                  'Europe': 3,
                  'South America': 4,
                  'Oceania': 5,
                  'Africa': 6
                 }
companies['Continent Number'] = companies['Continent'].replace(continent_dict)
print(companies.head())

# Create `Country/Region Numeric` column with numeric categories for Country/Region
companies['Country/Region Numeric'] = companies['Country/Region'].astype('category').cat.codes

# Convert `Industry` to numeric data
# Create dummy variables with Industry values
industry_encoded = pd.get_dummies(companies['Industry'])

# Combine `companies` DataFrame with new dummy Industry columns
companies = pd.concat([companies, industry_encoded], axis=1)

print(companies.head(10))
# Continent - Ordinal label encoding was used because there was a hierarchical order to the categories.
# Country/Region - Nominal label encoding was used because there was not a hierarchical order the categories.
# Industry - Dummy encoding was used because there were not many different categories represented and they were all equally important.
