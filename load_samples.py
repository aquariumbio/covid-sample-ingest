from util.pydent_helper import create_session
from util.sample_loader import load_samples_from_csv, create_items

session = create_session('laptop')

samples = load_samples_from_csv('test_specimens.csv', session, 'Specimen')

items = create_items(samples, session, 'Nasopharyngeal Swab', 'Ingest')