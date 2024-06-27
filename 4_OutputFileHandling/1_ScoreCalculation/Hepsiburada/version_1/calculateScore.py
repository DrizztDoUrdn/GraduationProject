import pandas as pd
import numpy as np

# Load the merged CSV file
file_path = '../../../1_FileMerginga/Hepsiburada/merged_hepsiburada_sentiment_normalized.csv'
merged_df = pd.read_csv(file_path)

# Replace 'missing' with NaN
merged_df['sentiment_category'].replace('missing', np.nan, inplace=True)
print(merged_df.columns)

# Group by product_name and calculate the mean sentiment score for each product
product_scores = merged_df.groupby(['product_id'])['sentiment_category'].mean().reset_index()

product_scores_with_names = pd.merge(product_scores, merged_df[['product_id', 'product_name']].drop_duplicates(), on='product_id')
product_scores_with_names = product_scores_with_names[['product_id', 'product_name', 'sentiment_category']]

# Save the product scores to a new CSV file
product_scores_with_names.to_csv('product_scores_hepsiburada.csv', index=False)

# Print the first few rows of the product scores to verify
print(product_scores.head())