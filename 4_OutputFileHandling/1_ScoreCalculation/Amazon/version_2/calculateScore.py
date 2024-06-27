import pandas as pd
import numpy as np

# Load the amazon CSV file
file_path = '../../../../Data/Amazon/4_NormalizedSentiment/version_2/unigram/normalized_amazon_tsln_final_case.tsv'
amazon_df = pd.read_csv(file_path, delimiter='\t')

# Replace 'missing' with NaN
amazon_df['sentiment_category'].replace('missing', np.nan, inplace=True)
print(amazon_df.columns)

# Group by product_name and calculate the mean sentiment score for each product
amazon_df = amazon_df.groupby(['product_id'])['sentiment_category'].mean().reset_index()

# Save the product scores to a new CSV file
amazon_df.to_csv('product_grouped_amazon.csv', index=False)

# Print the first few rows of the product scores to verify
print(amazon_df.head())
