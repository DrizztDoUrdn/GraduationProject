import csv
# Path to the CSV file
input_file_path = '../../../Data/Amazon/2_PreProcessedData/version_2/3_Lowercased/lowercased_comments.csv'
# Path to the output CSV file
output_file_path = '../../../Data/Amazon/2_PreProcessedData/version_2/4_Trimmed/trimmed_comments.csv'

# Function to find rows with more than 512 characters and write the trimmed rows to a new CSV file

def remove_long_rows(file_path, output_file_path, length_threshold=512):
    removed_count = 0
    with open(file_path, 'r', encoding='utf-8', newline='') as infile, \
            open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:

        csvreader = csv.reader(infile, delimiter=',')
        csvwriter = csv.writer(outfile, delimiter=',')

        for row in csvreader:
            # Check if the length of the third column exceeds the threshold
            if len(row[2]) <= length_threshold:
                # Write the row to the output file
                csvwriter.writerow(row)
            else:
                # Increment the counter for removed comments
                removed_count += 1

    return removed_count


# Remove rows with more than 512 characters and write the trimmed rows to a new CSV file
removed_comments = remove_long_rows(input_file_path, output_file_path)

print(f"Total number of comments removed: {removed_comments}")
print("Long rows removed")
