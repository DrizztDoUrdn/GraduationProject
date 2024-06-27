import pandas as pd

# Load the SentiTurkNet Excel file
file = 'STN.xlsx'
# Read the Excel file into a DataFrame
df = pd.read_excel(file)

df.iloc[:, 0] = df.iloc[:, 0].astype(str)

# Initialize an empty list to store processed word Data
words_data = []

# Function to determine the main polarity type
for index, row in df.iterrows():
    words = row[0].split(',')  # Split words by comma
    nscore = float(row[4])
    ntrscore = float(row[5])
    pscore = float(row[6])

    for word in words:
        word = word.strip()  # Remove leading/trailing whitespace

        # Calculate simple polarity score
        if max(nscore, ntrscore, pscore) == nscore:
            polarity: float = -nscore
        elif max(nscore, ntrscore, pscore) == ntrscore:
            polarity: float = 0
        else:
            polarity: float = pscore

        words_data.append((word, polarity))

# Optionally, save the updated DataFrame to a new Excel or CSV file
processed_df = pd.DataFrame(words_data, columns=['word', 'polarity'])

# Save to CSV
processed_df.to_csv('STN_main_polarity.csv', index=False)

# Print the DataFrame
print(processed_df.head())
