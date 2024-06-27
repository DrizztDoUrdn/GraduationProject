import pandas as pd

# Load the product scores CSV file
file_path = '../../1_ScoreCalculation/Hepsiburada/version_2/product_grouped_hepsiburada.csv'
product_scores = pd.read_csv(file_path)

# Define sentiment categories and their corresponding ranges
sentiment_categories = {
    (0.0, 0.2): 'çok kötü',
    (0.2, 0.3): 'kötü',
    (0.3, 0.4): 'idare eder',
    (0.4, 0.5): 'iyi',
    (0.5, 0.6): 'çok iyi'
}


# Map numerical sentiment scores to descriptive categories
def map_sentiment(score):
    for (lower, upper), label in sentiment_categories.items():
        if lower <= score < upper:
            return label
    return None  # Handle cases outside defined ranges


# Apply mapping function to the sentiment_category column
product_scores['sentiment_category'] = product_scores['sentiment_category'].apply(map_sentiment)

# Save the updated DataFrame to a new CSV file
output_file_path = 'mapped_hepsiburada.csv'
product_scores.to_csv(output_file_path, index=False)

# Print the first few rows of the updated DataFrame to verify
print(product_scores.head())
