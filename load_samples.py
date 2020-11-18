import os
import glob
import argparse

from util.pydent_helper import create_session
from util.sample_loader import load_samples_from_csv, create_items

def main():
    args = get_args()
    session = create_session(args.server)
    samples = []

    for file_path in glob.glob(os.path.join(args.path, "*.csv")):
        new_samples = load_samples_from_csv(file_path, session, "Specimen")
        samples.extend(new_samples)
        filename = os.path.basename(file_path)
        os.rename(file_path, os.path.join(args.archive_path, filename))

    create_items(samples, session, "Nasopharyngeal Swab", "Ingest")

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

if __name__ == "__main__":
    main()