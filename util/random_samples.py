import os
import datetime
import csv
import random
import string
import math

import namegenerator

def create_random_sample_csv(n_samples=96, filename_stub="specimens.csv", path="specimens_to_load"):
    ts = datetime.datetime.now()
    rack_barcode = random_string(16)

    fieldnames = [
        "name",
        "description",
        "project",
        "Specimen Barcode",
        "Rack Barcode",
        "Rack Location"
    ]
    rows = []

    for i in range(n_samples):
        rack_location = alphanum(i)
        row = {
            "name": "{}_{}".format(rack_barcode, rack_location),
            "description": "Specimen ingested at {} from rack {}".format(ts, rack_barcode),
            "project": "Test",
            "Specimen Barcode": random_string(16),
            "Rack Barcode": rack_barcode,
            "Rack Location": rack_location
        }
        rows.append(row)

    filename = "{}_{}".format(rack_barcode, filename_stub)
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

def alphanum(ind):
    alpha = "ABCDEFGH"
    return alpha[math.floor((ind) / 12)] + str((ind % 12) + 1)
