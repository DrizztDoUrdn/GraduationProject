import os
import csv

replacements = {
    'Beğenme Sayısı: ': '',
    'Dislike Sayısı: ': '',
    'Report: ': '',
    'Yorum: ': '',
    'Yıldız: ': ''
}


def replace_in_csv(csv_file_path):
    temp_file_path = csv_file_path + ".tmp"

    with (open(csv_file_path, 'r', encoding='utf-8') as infile,
          open(temp_file_path, 'w', encoding='utf-8', newline='') as outfile):
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        for row in reader:
            modified_row = []
            for cell in row:
                # Only replace if the cell starts with one of the keys
                for src, target in replacements.items():
                    if cell.startswith(src):
                        cell = cell.replace(src, target)
                        break  # Exit the inner loop after the first match
                modified_row.append(cell)  # Add the modified cell to the row

            writer.writerow(modified_row)  # Write the modified row

    os.remove(csv_file_path)
    os.rename(temp_file_path, csv_file_path)


csv_file_dir = '../../Data/Hepsiburada/1_RawData/version_0/2_csv_file/'
csv_files = [f for f in os.listdir(csv_file_dir) if f.endswith('.csv')]

for csv_file in csv_files:
    csv_file_path = os.path.join(csv_file_dir, csv_file)
    replace_in_csv(csv_file_path)
