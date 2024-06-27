from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import csv

f = 'C:/Users/deniz/PycharmProjects/pythonDeneme/Data/Hepsiburada/4_NormalizedSentiment/normalized_hepsiburada.tsv'
model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sa = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)

i, crr = 0, 0
with open(f, 'r', encoding='utf-8', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    next(csvreader)
    for row in csvreader:
        i += 1
        if i % 100 == 0:
            print(i)
        pred = sa(row[0])
        if pred and len(pred) > 0 and "label" in pred[0]:
            pred_label = pred[0]["label"]  # Extract the string label from the dictionary
            # Now you can use startswith on pred_label:
            if pred_label == "positive":
                pred_value = 1
            elif pred_label == "negative":
                pred_value = 0
            else:
                print(f"Warning: Unexpected label format '{pred_label}'")
                pred_value = None

            actual_label = row[1]

            if pred_value is not None and pred_value == int(actual_label):  # Compare labels
                crr += 1

print(crr, i, crr / i)
