import os
import pandas as pd

csv_file_dir = '../../../../../../Data/Amazon/3_ClassifiedData/version_2/TSLN/ngram/'
output_dir = '../../../../../../Data/Amazon/4_NormalizedSentiment/version_2/ngram/'


def normalize_sentiment(csv_file_path, output_file_path):
    df = pd.read_csv(csv_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'comment', 'max_sentiment'])

    # Create the 'sentiment_category' column based on the 'max_sentiment' values
    df['sentiment_category'] = df['max_sentiment'].apply(
        lambda x: 1 if x > 0 else 0
    )
    (df['sentiment_category']).head()
    df[['product_id', 'comment_id', 'comment', 'max_sentiment', 'sentiment_category']].to_csv(output_file_path, sep='\t', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith("ngram.csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"normalised_amazon_tsln_ngram.tsv")
        normalize_sentiment(input_file_path, output_file_path)
