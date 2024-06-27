import os
import pandas as pd

# Replace with the actual path to your lexicon CSV file
csv_file_dir = "../../../../../../Data/Amazon/2_PreProcessedData/version_2/3_Lowercased"
output_dir = "../../../../../../Data/Amazon/3_ClassifiedData"

lexicon = pd.read_csv('../../../../../../Dictionaries/TurkishSentiLiteralNet/turkish_sentiliteralnet.csv', sep=',', decimal='.')
lexicon = lexicon[[lexicon.columns[0], lexicon.columns[1]]].rename(
    columns={lexicon.columns[0]: 'word', lexicon.columns[1]: 'value'})

def analyze_sentiment_and_save(input_file_path, lexicon, output_file_path):
    """Calculates sentiment scores based on the third column and appends them to the CSV file."""
    df = pd.read_csv(input_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'text'])

    # Handle missing values in the 'text' column by setting the sentiment to 'missing' for those rows
    df['sentiment'] = df['text'].apply(lambda x: 'missing' if pd.isna(x) or x.strip() == '' else None)

    # Tokenize and 3_lowercase text in the third column, skipping rows with 'missing' sentiment
    df['words'] = df['text'].apply(lambda x: x.split() if pd.notna(x) and x.strip() != '' else [])

    # Explode into individual words, keeping original row index and renaming to 'word'
    data_exploded = df.explode('words').reset_index().rename(columns={'words': 'word'})

    # Join with lexicon on 'word', filter out rows without a match
    merged_df = data_exploded.merge(lexicon, on='word', how='inner')

    # Group by original index, sum sentiment values
    sentiment_scores = merged_df.groupby('index')['value'].sum()

    # Add sentiment scores back to the original DataFrame for rows without 'missing' sentiment
    df.loc[df['sentiment'].isnull(), 'sentiment'] = df.loc[df['sentiment'].isnull()].index.map(sentiment_scores)
    df['sentiment'] = df['sentiment'].apply(lambda x: 'NaN' if pd.isna(x) else x)

    # Save the DataFrame back to the CSV file, retaining the first and second columns
    df[['product_id', 'comment_id', 'text', 'sentiment']].to_csv(output_file_path, sep=',', index=False)


for filename in os.listdir(csv_file_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"analysed_amazon_tsln_final_case.csv")
        analyze_sentiment_and_save(input_file_path, lexicon, output_file_path)