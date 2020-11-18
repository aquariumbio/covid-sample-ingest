import csv
from util.pydent_helper import create_session
from util.random_samples import create_random_sample_csv

session = create_session('laptop')

create_random_sample_csv('test_specimens.csv')