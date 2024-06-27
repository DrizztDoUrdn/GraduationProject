import os
import pandas as pd

output_dir = '../../Data/Amazon/1_RawData/version_1/second_to_five_columns_extracted'
os.makedirs(output_dir, exist_ok=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df = pd.read_csv('../../Data/Hepsiburada/1_RawData/version_1/csv_file/urunler.csv', delimiter=',')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their types
print(df.info())

# Extract 2nd, 3rd, 4th, and 5th columns
extracted_columns = df.iloc[:, 1:5]

# Write the extracted columns to a new csv file
output_file_path = os.path.join(output_dir, 'second_to_five_columns.csv')
extracted_columns.to_csv(output_file_path, index=False)