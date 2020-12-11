import argparse
import os

def main():
    args = get_args()
    s = args.server
    p = args.path
    a = args.archive_path
    n = int(args.pool_number)
    o = int(args.plate_number)
    i = int(args.specimen_number)

    for _ in range(n * o):
        cmd = "python make_random_samples.py -n {}".format(i)
        os.system(cmd)

    cmd = "python load_samples.py -s {} -n {} -a {} -p {}".format(s, n, a, p)
    os.system(cmd)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="the path in which to find .csv files to load",
                        default="specimens_to_load")
    parser.add_argument("-a", "--archive-path",
                        help="the path in which to archive loaded .csv files",
                        default="loaded_specimens")
    parser.add_argument("-s", "--server",
                        help="the key pointing to the server instance in secrets.json",
                        default="laptop")
    parser.add_argument("-n", "--pool-number",
                        help="the number of specimens in a pool",
                        default="4")
    parser.add_argument("-o", "--plate-number",
                        help="the number of pooled plates you want to make",
                        default="1")
    parser.add_argument("-i", "--specimen-number",
                        help="the number of specimens per plate",
                        default="3")
    return parser.parse_args()

if __name__ == "__main__":
    main()