import pandas as pd
import numpy as np
import os

# Current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Data paths
data_file = os.path.join(current_dir, 'data/tao-all2.dat.gz')
column_names_file = os.path.join(current_dir, 'data/tao-all2.col')

# May use if necessary, but data seems less populated
small_data_file = os.path.join(current_dir, 'data/elnino.gz')
small_data_column_names_file = os.path.join(current_dir, 'data/elnino.col')

# Load column names
with open(column_names_file, 'r') as f:
    column_names = f.read().split()

# Read dataset & combine with column names
data = pd.read_csv(data_file, compression='gzip', delimiter=' ', header=None, names=column_names)

# Drop the 's.s.temp.' column because we will only use 'temp' column for geothermal visualization and because many rows contain missing values
data = data.drop(columns=['s.s.temp.'])

print(data)

# Replace '.' with NaN
data = data.replace('.', np.nan)

print(data)

# Remove rows with empty cells
data = data.dropna(how='any')

print(data)

# Sort the data by date
# NOTE: ONLY DO AFTER EVERYTHING ELSE IS FIGURED OUT
data = data.sort_values(by=['date','obs'])

# Save the cleaned data to a CSV file in the local directory
data.to_csv('data/cleaned_data.csv', index=False)