import datetime
from hashlib import blake2b
import csv

def create_random_sample_csv(filename):
    ts = datetime.datetime.now()
    batch_id = blake2b(str(ts).encode('utf-8'), digest_size=6).hexdigest()

    fieldnames = [
        'name',
        'description',
        'project',
        'Barcode ID'
    ]
    rows = []

    for i in range(1, 97):
        row = {
            'name': '{} #{:03d}'.format(batch_id, i),
            'description': 'Specimen ingested at {} from batch {}'.format(ts, batch_id),
            'project': 'Test',
            'Barcode ID': blake2b((batch_id + str(i)).encode('utf-8'), digest_size=6).hexdigest()
        }
        rows.append(row)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows: writer.writerow(row)