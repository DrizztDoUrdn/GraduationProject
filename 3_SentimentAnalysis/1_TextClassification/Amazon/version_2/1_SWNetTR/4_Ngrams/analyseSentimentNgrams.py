import pandas as pd
from itertools import islice

def generate_unigrams(tokens):
    """Generate unigrams from a list of tokens."""
    return tokens

def generate_bigrams(tokens):
    """Generate bigrams from a list of tokens."""
    bigrams = zip(tokens, islice(tokens, 1, None))
    return [' '.join(bigram) for bigram in bigrams]

def generate_trigrams(tokens):
    """Generate trigrams from a list of tokens."""
    trigrams = zip(tokens, islice(tokens, 1, None), islice(tokens, 2, None))
    return [' '.join(trigram) for trigram in trigrams]

def calculate_sentiment(df, lexicon, ngram_type):
    """Calculates sentiment scores based on n-grams."""
    if ngram_type == 'unigram':
        df['ngrams'] = df['comment'].str.split().apply(generate_unigrams)
    elif ngram_type == 'bigram':
        df['ngrams'] = df['comment'].str.split().apply(generate_bigrams)
    elif ngram_type == 'trigram':
        df['ngrams'] = df['comment'].str.split().apply(generate_trigrams)

    # Explode into individual n-grams, keeping original row index and renaming to 'ngram'
    data_exploded = df.explode('ngrams').reset_index().rename(columns={'ngrams': 'ngram'})

    # Join with lexicon on 'ngram', filter out rows without a match
    merged_df = data_exploded.merge(lexicon, left_on='ngram', right_on='word', how='inner')

    # Convert sentiment values to numeric data type
    merged_df['value'] = pd.to_numeric(merged_df['value'], errors='coerce')
    # Drop rows with missing or non-numeric sentiment values
    merged_df = merged_df.dropna(subset=['value'])

    # Group by original index, sum sentiment values
    sentiment_scores = merged_df.groupby('index')['value'].sum()

    # Add sentiment scores back to the original DataFrame
    df[f'{ngram_type}_sentiment'] = df.index.map(sentiment_scores).fillna(0)

    return df

def analyze_sentiment(input_file_path, lexicon, output_file_path):
    """Calculates sentiment scores based on unigrams, bigrams, and trigrams, and selects the highest score."""
    df = pd.read_csv(input_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'comment'])

    # Fill NaN values in the 'comment' column with an empty string
    df['comment'] = df['comment'].fillna('')

    # Calculate sentiment scores for unigrams, bigrams, and trigrams
    df = calculate_sentiment(df, lexicon, 'unigram')
    df = calculate_sentiment(df, lexicon, 'bigram')
    df = calculate_sentiment(df, lexicon, 'trigram')

    # Select the highest sentiment score for each comment
    df['max_sentiment'] = df[['unigram_sentiment', 'bigram_sentiment', 'trigram_sentiment']].max(axis=1)

    # Save the DataFrame back to the CSV file, retaining the first and second columns
    df[['product_id', 'comment_id', 'comment', 'max_sentiment']].to_csv(output_file_path, sep=',', index=False)

    return df

# Usage:
input_file_path = "../../../../../../Data/Amazon/2_PreProcessedData/version_2/4_Trimmed/trimmed_comments.csv"
lexicon_path = '../../../../../../Dictionaries/SW/Ngrams/Amazon/SWNetTR++_ngrams.csv'  # Path to your lexicon CSV file
output_file_path = '../../../../../../Data/Amazon/3_ClassifiedData/version_2/SWNetTR/ngram/analysed_amazon_swnet_ngram.csv'  # Path to save the output CSV file

# Load the lexicon
lexicon = pd.read_csv(lexicon_path, names=['word', 'value'])

# Analyze sentiment based on unigrams, bigrams, and trigrams
analyze_sentiment(input_file_path, lexicon, output_file_path)
