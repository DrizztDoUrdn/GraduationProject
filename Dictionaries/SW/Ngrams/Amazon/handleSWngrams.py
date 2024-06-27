import pandas as pd

def combine_csv_files(main_file_path, ngram_file_path, output_file_path):
    # Read the main CSV file into a DataFrame with ';' as delimiter and ',' as decimal separator
    main_df = pd.read_csv(main_file_path, delimiter=';', decimal=',')

    # Drop the 'polarity' column from the main DataFrame
    main_df = main_df.drop(columns=['polarity'])

    # Read the ngram CSV file into a DataFrame with ',' as delimiter and '.' as decimal separator
    ngram_df = pd.read_csv(ngram_file_path, delimiter=',', decimal='.')

    # Merge the two DataFrames on 'word' and 'tone' columns
    combined_df = pd.merge(main_df, ngram_df, on=['word', 'tone'], how='outer')

    # Save the combined DataFrame to a new CSV file with ',' as delimiter and '.' as decimal separator
    combined_df.to_csv(output_file_path, sep=',', decimal='.', index=False)

# Path to the input and output CSV files
main_file_path = 'SWNetTR++_ngrams.csv'
ngram_file_path = 'amazon_ngrams.csv'
output_file_path = 'SWNetTR++_ngrams.csv'

# Combine the CSV files and save the result to a new file
combine_csv_files(main_file_path, ngram_file_path, output_file_path)
