import os

input_dir = '../../Data/Hepsiburada/2_PreProcessedData/version_1/2_normalized/'
output_dir = "../../Data/Hepsiburada/2_PreProcessedData/version_1/3_lowercase/"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f'lowercase_urun_{filename.split('_')[-1]}')

        with (open(input_file_path, 'r', encoding='utf-8') as infile,
              open(output_file_path, 'w', encoding='utf-8') as outfile):
            for line in infile:
                modified_line = line.strip().lower()  # Remove leading/trailing whitespace and 3_lowercase
                outfile.write(modified_line + '\n')  # Add newline after each row
