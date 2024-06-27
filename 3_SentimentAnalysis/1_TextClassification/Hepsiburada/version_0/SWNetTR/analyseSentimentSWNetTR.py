import os
import csv
import pandas as pd

# Replace with the actual path to your lexicon CSV file
csv_file_dir = '../../../../../Data/Hepsiburada/2_PreProcessedData/version_1/3_lowercase'
output_dir = "../../../../../Data/Hepsiburada/3_ClassifiedData/"

lexicon = pd.read_csv('../../../../../Dictionaries/SW/SWNetTR++.csv', sep=';')  # Assuming format: WORD, POLARITY
lexicon = lexicon[[lexicon.columns[0], lexicon.columns[2]]].rename(
    columns={lexicon.columns[0]: 'word', lexicon.columns[2]: 'value'})


def analyze_sentiment_and_save(input_file_path, lexicon, output_file_path):
    """Calculates sentiment scores and appends them to the CSV file."""
    df = pd.read_csv(input_file_path, sep=',', header=1, names=['text'])

    # Tokenize and 3_lowercase text
    df['words'] = df['text'].str.split()

    # Explode into individual words, keeping original row index and renaming to 'word'
    data_exploded = df.explode('words').reset_index().rename(columns={'words': 'word'})

    # Join with lexicon on 'word', filter out rows without a match
    merged_df = data_exploded.merge(lexicon, on='word', how='inner')

    # Group by original index, sum sentiment values
    sentiment_scores = merged_df.groupby('index')['value'].sum()

    # Add sentiment scores back to original dataframe
    df['sentiment'] = sentiment_scores
    # Save the DataFrame back to the CSV file
    df[['text', 'sentiment']].to_csv(output_file_path, sep=',', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith("Hepsiburada.csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"analysed_hepsiburada.csv")  # Change the filename format
        analyze_sentiment_and_save(input_file_path, lexicon, output_file_path)
