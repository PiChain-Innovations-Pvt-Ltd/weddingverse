import pandas as pd
import os

# Path to the folder containing CSV files
folder_path = 'weddingbazaar/makeups/csv_loc_data'
# Output file name
output_file = 'combined_makeup_data.csv'

# List to hold all DataFrames
dataframes = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        # Read each CSV file and append the DataFrame to the list
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv(output_file, index=False)

print(f"All CSV files have been combined into {output_file}.")
