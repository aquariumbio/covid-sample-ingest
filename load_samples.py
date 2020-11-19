import argparse
from itertools import zip_longest

import pydent
from pydent import models
from pydent.models import Sample, Item, Plan
from pydent.exceptions import AquariumModelError

from util.pydent_helper import create_session
from util.sample_loader import load_all_in_path
from util.random_samples import random_name

def main():
    args = get_args()
    session = create_session(args.server)
    new_samples_by_filename = load_all_in_path(session, args.path, args.archive_path)

    plan = make_plan(session, "Test Plan")
    output_sample = make_output_sample(session)
    operations = []

    g = 0
    for filename, new_samples in new_samples_by_filename.items():
        g += 1
        operation = initialize_op(session, 'Pool Samples', 1024, 128*g)
        operation.associate("specimens_from_file", filename)

        # Can revive this if we need to set Options
        #
        # try:
        #     operation.set_input("Options", value={})
        # except AquariumModelError as err:
        #     print("FieldValue error: {0}".format(err))

        try:
            operation.set_input_array("Specimen", new_samples)
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

def initialize_op(session, name, x, y):
    op_type = session.OperationType.find_by_name(name)
    op = op_type.instance()
    op.x = x
    op.y = y
    return op

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