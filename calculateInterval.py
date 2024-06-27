import pandas as pd

# Path to the CSV file
file_path = 'Data/Amazon/3_ClassifiedData/version_2/analysed_amazon_tsln.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path,)

# Ensure the sentiment column is numeric
df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce')

# Drop rows with NaN values in the sentiment column
df = df.dropna(subset=['sentiment'])
df = df.dropna(subset=['text'])

# Filter out rows where the sentiment value is 0
df = df[df['sentiment'] != 0]
# Calculate the mean of the sentiment column
mean_sentiment = df['sentiment'].mean()

# Print the result
print(f"Mean of the sentiment column: {mean_sentiment}")
