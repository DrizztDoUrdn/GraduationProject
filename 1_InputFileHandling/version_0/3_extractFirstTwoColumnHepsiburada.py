import os
import csv

csv_file_dir = '../../Data/Hepsiburada/1_RawData/version_0/2_csv_file/'
first_two_columns_dir = os.path.join(csv_file_dir, '..', '3_first_two_columns_file')


os.makedirs(first_two_columns_dir, exist_ok=True)

for filename in os.listdir(csv_file_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(csv_file_dir, filename)

        first_two_columns_file_path = os.path.join(first_two_columns_dir, f"first_two_columns_{filename}")

        with open(input_file_path, 'r', encoding='utf-8') as infile, \
                \
                open(first_two_columns_file_path, 'w', encoding='utf-8', newline='') as first_two_outfile:

            reader = csv.reader(infile, delimiter=';')
            first_two_writer = csv.writer(first_two_outfile, delimiter=';')

            for row in reader:
                first_two_writer.writerow(row[:2])  # Write the first two columns
