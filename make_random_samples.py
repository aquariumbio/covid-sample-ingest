import csv
import argparse

from util.random_samples import create_random_sample_csv

def main():
    args = get_args()
    create_random_sample_csv(n_samples=int(args.n_samples))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_samples",
                        help="the number of samples to make",
                        default=96)
    return parser.parse_args()

if __name__ == "__main__":
    main()