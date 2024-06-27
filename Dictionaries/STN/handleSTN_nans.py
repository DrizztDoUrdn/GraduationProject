import pandas as pd

def clean_csv(input_file_path, output_file_path):
    # Read the CSV file
    df = pd.read_csv(input_file_path)

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Remove rows with 'nan' string in the 'word' column
    df = df[df['word'].str.lower() != 'nan']

    # Save the cleaned DataFrame back to a CSV file
    df.to_csv(output_file_path, index=False)

# Paths to input and output CSV files
input_file_path = 'STN_main_polarity.csv'
output_file_path = 'STN_main_polarity.csv'

# Clean the CSV file
clean_csv(input_file_path, output_file_path)
