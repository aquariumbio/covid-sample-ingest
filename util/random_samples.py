import os
import datetime
import csv
import random
import string

import namegenerator

def create_random_sample_csv(n_samples=96, filename_stub="specimens.csv", path="specimens_to_load"):
    ts = datetime.datetime.now()
    batch_id = random_string(16)

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
            "Barcode ID": random_string(16)
        }
        rows.append(row)

    filename = "{}_{}".format(batch_id, filename_stub)
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows: writer.writerow(row)

def random_string(length):
    alphanum = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphanum) for i in range(length))

def random_name():
    return namegenerator.gen()
