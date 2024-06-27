import pandas as pd

# Path to the Excel file
file_path = 'STN.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)

df.iloc[:, 0] = df.iloc[:, 0].astype(str)

# Initialize an empty list to store processed word Data
words_data = []


# Process each row in the DataFrame
for index, row in df.iterrows():
    words = row[0].split(',')  # Split words by comma
    nscore = float(row[4])
    ntrscore = float(row[5])
    pscore = float(row[6])

    for word in words:
        word = word.strip()  # Remove leading/trailing whitespace

        # Calculate simple polarity score
        simple_polarity = pscore - nscore

        # Calculate weighted polarity score

        words_data.append((word, simple_polarity))

# Create a DataFrame from the processed word Data
processed_df = pd.DataFrame(words_data, columns=['word', 'polarity'])

# Save to CSV
processed_df.to_csv('senti_turk_net.csv', index=False)

# Print the DataFrame
print(processed_df.head())
