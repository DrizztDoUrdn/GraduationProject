# remove stop words and drop noktalama isaretleri. +
# sayilar kalabilir onemli degil, yalniz emojileri de kaldirdi artik onu daha sonra hallederim

import csv
import os

import jpype
from jpype import JClass, JString

ZEMBEREK_PATH = 'C:/Users/deniz/java-zemberek/zemberek-full.jar'

# Start Jpype
jvm_args = ["-ea"]
jpype.startJVM(jpype.getDefaultJVMPath(), *jvm_args, classpath=[ZEMBEREK_PATH])

TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')

Token: JClass = JClass('zemberek.tokenization.Token')

tokenizer: TurkishTokenizer = TurkishTokenizer.DEFAULT


def remove_stop_words(tokens, stop_words):  # Take Zemberek tokens as input
    """Removes Turkish stop words from a list of Zemberek tokens."""
    filtered_tokens = []
    for token in tokens:
        if token.type not in {  # Access the type attribute on the Token object
            Token.Type.NewLine,
            Token.Type.SpaceTab,
            Token.Type.Punctuation,
            Token.Type.RomanNumeral,
            Token.Type.UnknownWord,
            Token.Type.Unknown
        } and str(token.content).lower() not in stop_words:
            filtered_tokens.append(token)
    return filtered_tokens


def spell_check_and_save(csv_file_path, tokenizer, output_file_path, stop_words):
    with open(csv_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8',
                                                                    newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        for row in reader:
            original_text = row[0]

            tokens: jpype.java.util.ArrayList = tokenizer.tokenize(JString(original_text))  # Tokenize the text

            filtered_tokens = remove_stop_words(tokens, stop_words)  # Remove stop words

            # Convert Zemberek tokens to strings before writing
            filtered_string_tokens = [str(token.content) for token in filtered_tokens]
            writer.writerow([" ".join(filtered_string_tokens)])


# Replace with the actual path to your stop words file
STOP_WORDS_FILE = "../../Dictionaries/SW/StopWordListTR.csv"

csv_file_dir = '../../Data/Hepsiburada/1_RawData/version_1/seventh_column_extracted/'
output_dir = '../../Data/Hepsiburada/2_PreProcessedData/version_1/1_stop_words_removed'

# Load stop words from file
with open(STOP_WORDS_FILE, 'r', encoding='utf-8') as stop_words_file:
    stop_words = set(word.strip() for word in stop_words_file)

# Process all CSV files in the directory
for filename in os.listdir(csv_file_dir):
    if filename.endswith('yorumlar.csv'):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        spell_check_and_save(input_file_path, tokenizer, output_file_path, stop_words)
