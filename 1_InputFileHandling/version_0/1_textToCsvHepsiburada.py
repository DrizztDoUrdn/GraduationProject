import os


def process_file(input_file_path, output_file_path):
    with open(text_file_path, 'r', encoding='utf-8') as f1, open(csv_file_path, 'w+', encoding='utf-8',
                                                                 newline='') as f2:
        lines = f1.read()
        for line in lines.split('\n'):
            if line.strip() == "":  # Skip empty lines
                continue
            elif line.startswith("Beğenme Sayısı"):
                f2.write("\n" + line + ";")
            else:
                f2.write(line + ";")


raw_data_dir = '../../Data/Hepsiburada/1_RawData/version_0'
text_file_dir = os.path.join(raw_data_dir, '1_text_file')
csv_file_dir = os.path.join(raw_data_dir, '2_csv_file')
os.makedirs(csv_file_dir, exist_ok=True)  # Create the output directory if it doesn't exist

text_files = [f for f in os.listdir(text_file_dir) if f.endswith('.txt')]

for text_file in text_files:
    text_file_path = os.path.join(text_file_dir, text_file)
    csv_file_name = os.path.splitext(text_file)[0] + '.csv'  # Get the base name and add .csv
    csv_file_path = os.path.join(csv_file_dir, csv_file_name)

    process_file(text_file_path, csv_file_path)
