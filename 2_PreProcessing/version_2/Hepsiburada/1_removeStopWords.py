import os
import re
import csv
import emoji
import jpype
from jpype import JClass, JString

ZEMBEREK_PATH = 'C:/Users/deniz/java-zemberek/zemberek-full.jar'

# Start Jpype
jvm_args = ["-ea"]
jpype.startJVM(jpype.getDefaultJVMPath(), *jvm_args, classpath=[ZEMBEREK_PATH])

TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')

Token: JClass = JClass('zemberek.tokenization.Token')

tokenizer: TurkishTokenizer = TurkishTokenizer.DEFAULT

def extract_emojis(text):
    emojis = [char for char in text if char in emoji.EMOJI_DATA]
    return ' '.join(emojis)

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


def check_stop_words(csv_file_path, tokenizer, output_file_path, stop_words,  emoji_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as infile, \
            open(output_file_path, 'w', encoding='utf-8', newline='') as outfile, \
            open(emoji_file_path, 'w', encoding='utf-8', newline='') as emoji_outfile:

        reader = csv.reader(infile, delimiter=',')
        writer = csv.writer(outfile, delimiter=',')
        emoji_writer = csv.writer(emoji_outfile, delimiter=',')

        for row in reader:
            original_text = row[2]

            # Extract emojis from the text
            emojis = extract_emojis(original_text)

            # Remove emojis from the original text
            text_without_emojis = re.sub(r'[^\w\s,]', '', original_text)

            # Tokenize the text without emojis
            tokens = tokenizer.tokenize(JString(text_without_emojis))

            # Remove stop words
            filtered_tokens = remove_stop_words(tokens, stop_words)

            # Convert Zemberek tokens to strings before writing
            filtered_string_tokens = [str(token.content) for token in filtered_tokens]

            # Combine filtered tokens and emojis
            final_text = " ".join(filtered_string_tokens) + " " + emojis

            writer.writerow([row[0], row[1], final_text])  # Write original columns plus the modified comment
            emoji_writer.writerow([row[1], " ".join(emojis)])  # Write comment_id and extracted emojis



# Replace with the actual path to your stop words file
STOP_WORDS_FILE = "../../../Dictionaries/SW/StopWordListTR.csv"

csv_file_dir = '../../../Data/Hepsiburada/1_RawData/version_2/ExtractedColumns/'
output_dir = '../../../Data/Hepsiburada/2_PreProcessedData/version_2/1_StopWordsRemoved'
os.makedirs(output_dir, exist_ok=True)


# Load stop words from file
with open(STOP_WORDS_FILE, 'r', encoding='utf-8') as stop_words_file:
    stop_words = set(word.strip() for word in stop_words_file)

# Process all CSV files in the directory
for filename in os.listdir(csv_file_dir):
    if filename.endswith('extracted_columns.csv'):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"stopwords_removed.csv")
        emoji_file_path = '../../../Data/Hepsiburada/1_RawData/version_2/Emojis/emojis.csv'

        check_stop_words(input_file_path, tokenizer, output_file_path, stop_words, emoji_file_path)

