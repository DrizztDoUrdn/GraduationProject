import pandas as pd
import numpy as np

# Load the Hepsiburada CSV file
file_path = '../../../../Data/Hepsiburada/4_NormalizedSentiment/version_2/unigram/normalized_hepsiburada_tsln_final_case.tsv'
hepsiburada_df = pd.read_csv(file_path, delimiter='\t')

# Replace 'missing' with NaN
hepsiburada_df['sentiment_category'].replace('missing', np.nan, inplace=True)
print(hepsiburada_df.columns)

# Group by product_name and calculate the mean sentiment score for each product
hepsiburada_df = hepsiburada_df.groupby(['product_id'])['sentiment_category'].mean().reset_index()

# Save the product scores to a new CSV file
hepsiburada_df.to_csv('product_grouped_hepsiburada.csv', index=False)

# Print the first few rows of the product scores to verify
print(hepsiburada_df.head())
