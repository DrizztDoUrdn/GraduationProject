import csv
import os
from pathlib import Path

import jpype
from jpype.types import *

# Data path
DATA_PATH = Path('../../Data/Hepsiburada/1_RawData')
# Zemberek Path
ZEMBEREK_PATH = 'C:/Users/deniz/java-zemberek/zemberek-full.jar'

# Start Jpype
jvm_args = ["-ea"]
jpype.startJVM(jpype.getDefaultJVMPath(), *jvm_args, classpath=[ZEMBEREK_PATH])

TurkishSpellChecker: JClass = JClass(
    'zemberek.normalization.TurkishSpellChecker'
)
TurkishTokenizer: JClass = JClass('zemberek.tokenization.TurkishTokenizer')
TurkishLexer: JClass = JClass('zemberek.tokenization.antlr.TurkishLexer')
TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
Token: JClass = JClass('zemberek.tokenization.Token')


def spell_check_and_save(csv_file_path, tokenizer, spell_checker, output_file_path):
    """Spell checks the CSV file, row by row, and saves the corrected document to a new file."""
    with open(csv_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8',
                                                                    newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        for row in reader:
            original_text = row[0]  # Get text from the first (and only) column
            tokens = tokenizer.tokenize(JString(original_text))

            corrected_tokens = []
            for token in tokens:
                if token.type not in {
                    Token.Type.NewLine,
                    Token.Type.SpaceTab,
                    Token.Type.Punctuation,
                    Token.Type.RomanNumeral,
                    Token.Type.UnknownWord,
                    Token.Type.Unknown
                } and not spell_checker.check(token.content):
                    suggestions = list(spell_checker.suggestForWord(token.content))
                    if suggestions:
                        suggestion = str(suggestions[0])
                        print(f'Correction: {token.content} -> {suggestion}.')
                        corrected_tokens.append(suggestion)
                        continue
                corrected_tokens.append(str(token.content))

            writer.writerow(["".join(corrected_tokens)])  # Write corrected text as a single row in the new file


csv_file_dir = '../../Data/Hepsiburada/2_PreProcessedData/version_1/1_stop_words_removed'  # Path to your CSV files
output_dir = '../../Data/Hepsiburada/2_PreProcessedData/version_1/2_normalized'

os.makedirs(output_dir, exist_ok=True)

tokenizer: TurkishTokenizer = TurkishTokenizer.ALL
morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()
spell_checker: TurkishSpellChecker = TurkishSpellChecker(morphology)

for filename in os.listdir(csv_file_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        # Extract the file number from the filename and use it for the output filename
        file_number = filename.split("_")[-1].split(".")[0]
        output_file_path = os.path.join(output_dir, f"normalized_urun_{file_number}.csv")

        spell_check_and_save(input_file_path, tokenizer, spell_checker, output_file_path)
