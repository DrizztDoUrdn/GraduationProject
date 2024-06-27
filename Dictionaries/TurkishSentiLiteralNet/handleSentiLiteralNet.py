import xml.etree.ElementTree as ET
import csv


def convert_xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "polarity"])

        for word in root.findall('WORD'):
            name = word.find('NAME').text
            pscore = float(word.find('PSCORE').text)
            nscore = float(word.find('NSCORE').text)

            # Calculate polarity
            polarity_score = pscore - nscore
            if polarity_score > 0:
                polarity = polarity_score
            elif polarity_score < 0:
                polarity = polarity_score
            else:
                polarity = polarity_score

            writer.writerow([name, polarity])


# Example usage
xml_file = 'turkish_sentiliteralnet.xml'  # Replace with your XML file path
csv_file = 'turkish_sentiliteralnet.csv'  # Replace with your desired output CSV file path

convert_xml_to_csv(xml_file, csv_file)
