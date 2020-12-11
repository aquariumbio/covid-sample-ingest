import argparse
import sys

from itertools import islice

import pydent
from pydent.exceptions import AquariumModelError

from util.pydent_helper import create_session
from util.sample_loader import load_all_in_path, get_rack_barcode
from util.random_samples import random_name

POOL_SAMPLES_OPERATION = "Pool Samples"

def main():
    args = get_args()
    session = create_session(args.server)
    new_samples_by_filename = load_all_in_path(session, args.path, args.archive_path)
    pool_number = int(args.pool_number)

    for pool_group in pool_groups(new_samples_by_filename, pool_number):
        output_sample = make_output_sample(session)
        operations = []
        included_racks = []

        g = 0
        for filename, new_samples in pool_group.items():
            g += 1
            operation = make_operation(session, 1024, 128*g)
            operation.associate("specimens_from_file", filename)

            try:
                operation.set_input_array("Specimen", new_samples)
                operation.set_output("Pooled Sample Plate", sample=output_sample)
            except AquariumModelError as err:
                print("FieldValue error: {0}".format(err))

            operations.append(operation)
            included_racks.append(get_rack_barcode(filename))

        plan_name = "{}: {}".format(output_sample.name, ", ".join(included_racks))
        plan = make_plan(session, plan_name)
        plan.add_operations(operations)
        plan.save()

        user = session.User.find_by_name("Joe Neptune")
        budget = session.Budget.find_by_name("My First Budget")
        plan.submit(user, budget)

def make_operation(session, x, y):
    """Make an operation and set x and y coordinates for the designer

    """
    op_type = session.OperationType.find_by_name(POOL_SAMPLES_OPERATION)
    op = op_type.instance()
    op.x = x
    op.y = y
    return op

def make_output_sample(session):
    """Make an output sample with a randomly-generated name.

    """
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
    """Make a new plan.

    """
    plan = session.Plan.new(name=name)
    plan.create()
    return plan

def pool_groups(data, size):
    """Split data into chunks.

    """
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="the path in which to find .csv files to load",
                        default="specimens_to_load")
    parser.add_argument("-a", "--archive-path",
                        help="the path in which to archive loaded .csv files",
                        default="loaded_specimens")
    parser.add_argument("-s", "--server",
                        help="the key pointing to the server instance in secrets.json")
    parser.add_argument("-n", "--pool-number",
                        help="the number of specimens in a pool")
    return parser.parse_args()

if __name__ == "__main__":
    main()