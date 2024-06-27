import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 512}
tokenizer = AutoTokenizer.from_pretrained("mdeniz1/turkish-sentiment-analysis-bert-base-turkish-uncased")
# Load your model
model = pipeline("text-classification", model="mdeniz1/turkish-sentiment-analysis-bert-base-turkish-uncased",
                 tokenizer=tokenizer, **tokenizer_kwargs)

f = ('C:/Users/deniz/PycharmProjects/pythonDeneme/Data/Amazon/4_NormalizedSentiment/version_2/ngram'
     '/normalised_amazon_tsln_ngram.tsv')

# Read the TSV file into a DataFrame
df = pd.read_csv(f, sep='\t')

# Drop the 4th column (index 3)
df.drop(df.columns[3], axis=1, inplace=True)

total_count = 0
correct_count = 0
incorrect_predictions = []

true_positives = 0
false_positives = 0
false_negatives = 0

# Iterate over the DataFrame rows

for index, row in df.iterrows():
    total_count += 1
    if total_count % 100 == 0:
        print(total_count)

    text = row['comment']
    actual_label = int(row['sentiment_category'])

    # Skip rows with NaN values in the text column
    if pd.isna(text):
        continue

    # Predict sentiment
    pred = model(text)
    pred_label = pred[0]["label"]
    if pred_label == "LABEL_2":  # LABEL_2 Pos
        pred_value = 1
    elif pred_label == 'LABEL_1':  # LABEL_1 Neutral
        pred_value = -1
    elif pred_label == "LABEL_0":  # Label_0 Negative
        pred_value = 0

    # Compare predicted label with actual label
    if pred_value is not None and pred_value == actual_label:
        correct_count += 1
        if actual_label == 1:
            true_positives += 1
    else:
        # Save
        incorrect_predictions.append({
            'comment': text,
            'actual_label': actual_label,
            'predicted_label': pred_value
        })
        if actual_label == 1:
            false_negatives += 1
        elif pred_value == 1:
            false_positives += 1

# Calculate accuracy
accuracy = correct_count / total_count if total_count > 0 else 0

# Calculate precision, recall, and F1 score
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print("Correct Predictions:", correct_count)
print("Total Predictions:", total_count)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

wrong_predictions_df = pd.DataFrame(incorrect_predictions)
wrong_predictions_df.to_csv('amazon_wrong_predictions.csv', index=False)
