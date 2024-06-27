import os
import pandas as pd

csv_file_dir = '../../../../../../Data/Amazon/3_ClassifiedData/version_2/SWNetTR/unigram/'
output_dir = '../../../../../../Data/Amazon/4_NormalizedSentiment/version_2/SWNetTR/unigram'


def normalize_sentiment(csv_file_path, output_file_path):
    df = pd.read_csv(csv_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'comment', 'sentiment'])

    # Create the 'sentiment_category' column based on the 'sentiment' values
    df['sentiment_category'] = df['sentiment'].apply(
        lambda x: 1 if x > 0 else 0
    )
    (df['sentiment_category']).head()
    df[['product_id', 'comment_id', 'comment', 'sentiment', 'sentiment_category']].to_csv(output_file_path, sep='\t', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith("analysed_amazon_swnet_unigram.csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"normalized_amazon_swnet_unigram.tsv")
        normalize_sentiment(input_file_path, output_file_path)
