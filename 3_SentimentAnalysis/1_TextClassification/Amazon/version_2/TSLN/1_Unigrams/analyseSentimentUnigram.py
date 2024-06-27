import os
import pandas as pd

csv_file_dir = "../../../../../../Data/Amazon/2_PreProcessedData/version_2/4_Trimmed"
output_dir = "../../../../../../Data/Amazon/3_ClassifiedData/version_2/TSLN/unigram"

lexicon = pd.read_csv('../../../../../../Dictionaries/TurkishSentiLiteralNet/turkish_sentiliteralnet.csv', sep=',', decimal='.')
lexicon = lexicon[[lexicon.columns[0], lexicon.columns[1]]].rename(
    columns={lexicon.columns[0]: 'word', lexicon.columns[1]: 'value'})


def analyze_sentiment_and_save(input_file_path, lexicon, output_file_path):
    """Calculates sentiment scores based on the third column and appends them to the CSV file."""
    df = pd.read_csv(input_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'comment'])

    # Tokenize text
    df['words'] = df['comment'].str.split()

    # Explode into individual words, keeping original row index and renaming to 'word'
    data_exploded = df.explode('words').reset_index().rename(columns={'words': 'word'})

    # Join with lexicon on 'word', filter out rows without a match
    merged_df = data_exploded.merge(lexicon, on='word', how='inner')

    # Group by original index, sum sentiment values
    sentiment_scores = merged_df.groupby('index')['value'].sum()

    # Add sentiment scores back to the original DataFrame
    df['sentiment'] = df.index.map(sentiment_scores).fillna(0)  # Fill missing scores with nan?

    # Save the DataFrame back to the CSV file, retaining the first and second columns
    df[['product_id', 'comment_id', 'comment', 'sentiment']].to_csv(output_file_path, sep=',', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"analysed_amazon_tsln_unigram.csv")
        analyze_sentiment_and_save(input_file_path, lexicon, output_file_path)
