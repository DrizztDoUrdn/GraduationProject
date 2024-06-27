import pandas as pd

# Load your CSV files
df_comments = pd.read_csv(
    '../../Data/Hepsiburada/1_RawData/version_1/second_to_five_columns_extracted/second_to_five_columns.csv')
df_sentiment = pd.read_csv('../../Data/Hepsiburada/3_ClassifiedData/version_1/analysed_hepsiburada.csv')

# Extract comment_id values into a list
comment_ids = df_comments['comment_id'].tolist()

# Add comment_id column to df_sentiment
df_sentiment['comment_id'] = comment_ids

# Merge the DataFrames
merged_df = pd.merge(df_comments, df_sentiment, on='comment_id', how='left')

# Save the merged results
merged_df.to_csv('../../Data/Hepsiburada/product_score/product_score.csv', index=False)