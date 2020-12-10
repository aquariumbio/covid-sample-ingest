import os
import datetime
import csv
import random
import string
import math

import namegenerator

def create_random_sample_csv(n_samples=96, path="specimens_to_load"):
    ts = datetime.datetime.now().strftime('%Y%m%d')
    stub = random_stub()

    fieldnames = [
        "Column",
        "Row",
        "Code"
    ]
    rows = []

    for i in range(n_samples):
        rack_location = alphanum(i)
        row = {
        "Column": rack_location["num"],
        "Row": rack_location["alpha"],
        "Code": random_code(stub)
        }
        rows.append(row)

    rows.sort(key=lambda x: [x["Column"], x["Row"]])

    filename = "{}-{}.txt".format(ts, random_number())
    file_path = os.path.join(path, filename)
    with open(file_path, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writerow({})
        writer.writerow({})
        writer.writeheader()
        for row in rows:
            writer.writerow({})
            writer.writerow(row)
        writer.writerow({})

def random_string(length):
    alphanum = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphanum) for i in range(length))

def random_stub():
    alpha = ''.join(random.choice(string.ascii_uppercase) for i in range(2))
    num = random_number()
    return alpha + num

def random_code(stub):
    return stub + ''.join(random.choice(string.digits) for i in range(4))

def random_number():
    return ''.join(random.choice(string.digits) for i in range(6))

def random_name():
    return namegenerator.gen()

def alphanum(ind):
    alpha = "ABCDEFGH"
    return {
        "alpha": alpha[math.floor((ind) / 12)],
        "num": "{:0>2d}".format((ind % 12) + 1)
    }
