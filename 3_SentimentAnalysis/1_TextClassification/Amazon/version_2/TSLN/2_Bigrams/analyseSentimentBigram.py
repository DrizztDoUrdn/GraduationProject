import pandas as pd
from itertools import islice

input_file_path = '../../../../../../Data/Amazon/2_PreProcessedData/version_2/4_Trimmed/trimmed_comments.csv'
output_file_path = '../../../../../../Data/Amazon/3_ClassifiedData/version_2/TSLN/bigram/analysed_amazon_tsln_bigram.csv'

lexicon = pd.read_csv('../../../../../../Dictionaries/TurkishSentiLiteralNet/Ngrams/Amazon/turkish_sentiliteralnet_ngrams.csv', sep=',', decimal='.')
lexicon = lexicon[[lexicon.columns[0], lexicon.columns[1]]].rename(
    columns={lexicon.columns[0]: 'word', lexicon.columns[1]: 'value'})


def generate_bigrams(tokens):
    """Generate bigrams from a list of tokens."""
    bigrams = zip(tokens, islice(tokens, 1, None))
    return [' '.join(bigram) for bigram in bigrams]


def analyze_sentiment_bigram(input_file_path, lexicon, output_file_path):
    """Calculates sentiment scores based on bigrams in the third column and appends them to the CSV file."""
    df = pd.read_csv(input_file_path, sep=',', header=0, names=['product_id', 'comment_id', 'comment'])

    # Fill NaN values in the 'comment' column with an empty string
    df['comment'] = df['comment'].fillna('')

    # Tokenize text in the third column and generate bigrams
    df['bigrams'] = df['comment'].str.split().apply(generate_bigrams)

    # Explode into individual bigrams, keeping original row index and renaming to 'bigram'
    data_exploded = df.explode('bigrams').reset_index().rename(columns={'bigrams': 'bigram'})

    # Join with lexicon on 'bigram', filter out rows without a match
    merged_df = data_exploded.merge(lexicon, left_on='bigram', right_on='word', how='inner')

    # Group by original index, sum sentiment values
    sentiment_scores = merged_df.groupby('index')['value'].sum()

    # Add sentiment scores back to the original DataFrame
    df['sentiment'] = df.index.map(sentiment_scores).fillna(0)

    # Save the DataFrame back to the CSV file, retaining the first and second columns
    df[['product_id', 'comment_id', 'comment', 'sentiment']].to_csv(output_file_path, sep=',', index=False)


analyze_sentiment_bigram(input_file_path, lexicon, output_file_path)
