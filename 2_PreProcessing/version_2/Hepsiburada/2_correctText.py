import csv
import os
import jpype
from jpype.types import *

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


def correct_text(csv_file_path, tokenizer, spell_checker, output_file_path):
    """Spell checks the CSV file, row by row, and saves the corrected document to a new file."""
    with (open(csv_file_path, 'r', encoding='utf-8') as infile,
          open(output_file_path, 'w', encoding='utf-8', newline='') as outfile):
        reader = csv.reader(infile, delimiter=',')
        writer = csv.writer(outfile, delimiter=',')

        for row in reader:
            original_text = row[2]  # Get text from the first (and only) column
            # Tokenize the original text
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

            new_row = row[:2] + [" ".join(corrected_tokens)]
            writer.writerow(new_row)


csv_file_dir = '../../../Data/Hepsiburada/2_PreProcessedData/version_2/1_StopWordsRemoved'
output_dir = '../../../Data/Hepsiburada/2_PreProcessedData/version_2/2_TextCorrected'

os.makedirs(output_dir, exist_ok=True)

tokenizer: TurkishTokenizer = TurkishTokenizer.ALL
morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()
spell_checker: TurkishSpellChecker = TurkishSpellChecker(morphology)

for filename in os.listdir(csv_file_dir):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(csv_file_dir, filename)
        output_file_path = os.path.join(output_dir, f"corrected_comments.csv")
        correct_text(input_file_path, tokenizer, spell_checker, output_file_path)