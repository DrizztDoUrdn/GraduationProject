import pandas as pd

mapped_csv_file = '../../2_RecordMapping/hepsiburada/mapped_hepsiburada.csv'
product_name_file = '../../../Data/Hepsiburada/1_RawData/version_2/CsvFile/urunler.csv'
output_csv_file = 'final_one_hepsiburada.csv'


def merge_and_save(mapped_file, product_file, output_csv_file):
    # Read product CSV file
    product_df = pd.read_csv(mapped_file)

    # Read sentiment CSV file
    sentiment_df = pd.read_csv(product_file)

    # Merge DataFrames based on the 'product_id' column
    merged_df = pd.merge(sentiment_df, product_df, on='product_id', how='left')

    unique_df = merged_df[['product_id', 'product_name', 'sentiment_category']].drop_duplicates()

    # Select necessary columns
    final_df = unique_df[['product_id', 'product_name', 'sentiment_category']]

    # Save the final DataFrame to a new CSV file
    final_df.to_csv(output_csv_file, index=False)


merge_and_save(mapped_csv_file, product_name_file, output_csv_file)
