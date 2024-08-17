import csv
import sys
import xml.etree.ElementTree as ET

# Convert SafeInCloud XML export file to 1Password CSV import file
# easylob@gmail.com

def main():
    print('\nSafe in Cloud XML => 1Password CSV')

    xml_file = None
    csv_file = None
    if len(sys.argv) == 3:
        xml_file = sys.argv[1]
        csv_file = sys.argv[2]
    if xml_file is None or csv_file is None:
        print('python sic_to_1password.py SafeInCloud.xml 1Password.csv')
        exit()

    labels = extract_labels_from_xml(xml_file)
    data = extract_data_from_xml(xml_file, labels)
    write_data_to_csv(csv_file, data)

    print(f'{xml_file} => {csv_file}')
 
def extract_labels_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    labels = []

    for label in root.findall('.//label'):
        label_data = {
            'id': label.get('id'),
            'label': label.get('name')
        }
        #print(label_data)
        labels.append(label_data)

    return labels

def extract_data_from_xml(xml_file, labels):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []

    # Convert just N accounts, for testing purposes
    n = 999999
    nn = 0
    for card in root.findall('.//card'):
        title = card.get('title')

        # DO NOT Convert some accounts
        #if title.startswith('Z '):
        #    print(title)
        #    continue
                
        card_data = {
            'title': title,
            'login': '',
            'password': '',
            'website': '',
            'notes': '',
            'label': '',
        }

        # <field>
        for field in card.findall('field'):
            field_type = field.get('type')
            if field_type in card_data:
                card_data[field_type] = field.text

        # <note>
        note = card.findall('notes')
        if len(note) > 0:
            card_data['notes'] = note[0].text

        # <label_id>
        label_id = card.findall('label_id')
        if len(label_id) > 0:
            label = [label for label in labels if label.get('id') == label_id[0].text]
            #label = any(label for label in labels if labels.get('id') == label_id[0].text)
            if len(label) > 0:                
                card_data['label'] = label[0].get('label')

        #if not (card_data['login'] is None or card_data['login'] == ''):
        #print(card_data)
        data.append(card_data)

        nn = nn + 1
        if (nn > n):
            break

    return data

def write_data_to_csv(csv_file, data):
    fieldnames = ['title', 'login', 'password', 'website', 'notes', 'label']
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    main()
