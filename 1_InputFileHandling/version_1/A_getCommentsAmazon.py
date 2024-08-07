import csv
import os

csv_file_dir = '../../Data/Amazon/1_RawData/version_1/csv_file/'
output_dir = os.path.join(csv_file_dir, '..', 'TestFile')
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(csv_file_dir):
    if filename.endswith("yorumlar.csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"comments_column_{filename}")

        with (open(input_file_path, 'r', encoding='utf-8') as infile,
              open(output_file_path, 'w', encoding='utf-8', newline='') as outfile):
            reader = csv.reader(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
            writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                if len(row) >= 5:
                    writer.writerow([row[3]])  # Write only the fourth column
