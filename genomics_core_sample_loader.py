import csv
from util.pydent_helper import create_session
from util.sample_loader import create_random_sample_csv, load_samples_from_csv, create_items

session = create_session('duke_covid_sandbox')

create_random_sample_csv('test_specimens.csv')

samples = load_samples_from_csv('test_specimens.csv', session, 'Specimen')

items = create_items(samples, session, 'Nasopharyngeal Swab', 'Ingest')