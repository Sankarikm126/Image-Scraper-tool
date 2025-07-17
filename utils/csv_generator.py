import csv

def generate_csv(data, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['page_url', 'image_url', 'image_name', 'alt_text'])
        writer.writeheader()
        for row in data:
            writer.writerow({
                'page_url': row['page_url'],
                'image_url': row['image_url'],
                'image_name': row['image_name'],
                'alt_text': row['alt_text']
            })
