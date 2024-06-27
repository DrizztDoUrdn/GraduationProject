import pandas as pd
import os

input_dir = '../../../Data/Amazon/2_PreProcessedData/version_2/2_TextCorrected/'
output_dir = "../../../Data/Amazon/2_PreProcessedData/version_2/3_Lowercased/"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith("without_spaces.csv"):
        input_file_path = os.path.join(input_dir, filename)

        # Read the entire CSV file
        df = pd.read_csv(input_file_path)

        # Check if the CSV has at least three columns
        if len(df.columns) >= 3:
            # 3_Lowercased the third column (index 2)
            df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.lower()

            # Save the modified DataFrame to a new CSV file
            output_file_path = os.path.join(output_dir, f'Lowercased_comments.csv')
            df.to_csv(output_file_path, index=False)  # Save without row indices
        else:
            print(f"Skipping file {filename} as it does not have at least three columns.")
