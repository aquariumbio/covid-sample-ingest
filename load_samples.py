import os
import glob
import argparse
from itertools import zip_longest

import pydent
from pydent import models
from pydent.models import Sample, Item, Plan
from pydent.exceptions import AquariumModelError

from util.pydent_helper import create_session
from util.sample_loader import load_samples_from_csv, create_items
from util.random_samples import random_name

def main():
    args = get_args()
    session = create_session(args.server)
    samples = load_all_in_path(session, args.path, args.archive_path)
    items = create_items(samples, session, "Nasopharyngeal Swab", "Ingest")
    # items = sorted(session.Item.last(3*96), key=lambda x: x.sample_id)
    grouped_items = grouper(96, items, fillvalue=None)

    plan = make_plan(session, "Test Plan")
    output_sample = make_output_sample(session)
    operations = []

    for g, item_group in enumerate(grouped_items, start=1):
        item_group = list(filter(None, item_group))
        operation = initialize_op(session, 'Pool Samples', 1024, 128*g)

        # Can revive this if we need to set Options
        #
        # try:
        #     operation.set_input("Options", value={})
        # except AquariumModelError as err:
        #     print("FieldValue error: {0}".format(err))

        object_type = session.ObjectType.find_by_name("Nasopharyngeal Swab")
        all_values = [values(item, object_type) for item in item_group]

        try:
            operation.set_input_array("Specimen", all_values)
            operation.set_output("Pooled Sample Plate", sample=output_sample)
        except AquariumModelError as err:
            print("FieldValue error: {0}".format(err))

        operations.append(operation)

    plan.add_operations(operations)
    plan.save()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="the path in which to find .csv files to load",
                        default="specimens_to_load")
    parser.add_argument("-a", "--archive_path",
                        help="the path in which to archive loaded .csv files",
                        default="loaded_specimens")
    parser.add_argument("-s", "--server",
                        help="the key pointing to the server instance in secrets.json")
    return parser.parse_args()

def load_all_in_path(session, path, archive_path):
    samples = []
    for file_path in glob.glob(os.path.join(path, "*.csv")):
        new_samples = load_samples_from_csv(file_path, session, "Specimen")
        samples.extend(new_samples)
        filename = os.path.basename(file_path)
        os.rename(file_path, os.path.join(archive_path, filename))
    return samples

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def initialize_op(session, name, x, y):
    op_type = session.OperationType.find_by_name(name)
    op = op_type.instance()
    op.x = x
    op.y = y
    return op

def values(item, object_type):
    return {
        "sample": item.sample,
        "container": object_type,
        "item": item
    }

def make_output_sample(session):
    output_sample = session.Sample.new(
        name=random_name(),
        description="",
        project="Test",
        sample_type=session.SampleType.find_by_name("Pooled Specimens"),
        properties={"Test": "foo"}
    )
    output_sample.save()
    return output_sample

def make_plan(session, name):
    plan = session.Plan.new(name=name)
    plan.create()
    return plan

if __name__ == "__main__":
    main()