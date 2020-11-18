import os
import datetime
from hashlib import blake2b
import csv

def create_random_sample_csv(n_samples=96, filename_stub="specimens.csv", path="specimens_to_load"):
    ts = datetime.datetime.now()
    batch_id = blake2b(str(ts).encode("utf-8"), digest_size=6).hexdigest()

    fieldnames = [
        "name",
        "description",
        "project",
        "Barcode ID"
    ]
    rows = []

    for i in range(1, n_samples + 1):
        row = {
            "name": "{} #{:03d}".format(batch_id, i),
            "description": "Specimen ingested at {} from batch {}".format(ts, batch_id),
            "project": "Test",
            "Barcode ID": blake2b((batch_id + str(i)).encode("utf-8"), digest_size=6).hexdigest()
        }
        rows.append(row)

    filename = "{}_{}".format(batch_id, filename_stub)
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows: writer.writerow(row)