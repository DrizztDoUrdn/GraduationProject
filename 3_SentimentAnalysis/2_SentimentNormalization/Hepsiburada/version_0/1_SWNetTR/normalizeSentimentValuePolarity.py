import os
import pandas as pd

csv_file_dir = '../../../../../Data/Hepsiburada/3_ClassifiedData/'
output_dir = '../../../../../Data/Hepsiburada/4_NormalizedSentiment/'  # Save in the same directory


def csv_to_tsv(csv_file_path, output_file_path):
    """Calculates sentiment scores and saves them to a new CSV file in the output directory."""
    df = pd.read_csv(csv_file_path, sep=',', header=0)
    df['sentiment'] = df['sentiment'].fillna(0)  # Replace NaN with 0 (or another default value)

    df_filtered = df[df['sentiment'] != 0].copy()  # Explicitly copy the filtered DataFrame
    df_filtered.loc[:, 'sentiment_category'] = df_filtered['sentiment'].apply(
        lambda x: 1 if x > 0 else 0
    )

    # Select only 'text' and 'sentiment_category' columns before saving
    df_filtered[['text', 'sentiment_category']].to_csv(output_file_path, sep='\t', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith("tone.csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"normalized_hepsiburada_tone.tsv")
        csv_to_tsv(input_file_path, output_file_path)
