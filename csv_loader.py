import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_csv(delimiter=',', encoding=None):
    # Open file dialog to select CSV file
    Tk().withdraw() # Hide the Tkinter root window
    file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    try:
        # Load CSV file into a pandas dataframe
        df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
   # Check for null and NaN values
    null_count = df.isnull().sum().sum()
    na_count = df.isna().sum().sum()
    if null_count > 0 or na_count > 0:
        print(f"Warning: CSV file contains {null_count+na_count} null or NaN values.")
        print(f"* {null_count} null values")
        print(f"* {na_count} NaN values")
        
    # Print summary of loaded CSV file
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns from {file_path}:")
    print(df.head())
    
    return df

df=load_csv()