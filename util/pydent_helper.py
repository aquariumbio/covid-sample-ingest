import os
import json
import pydent
from pydent import AqSession, __version__

def create_session(aq_instance):
    """
    Create a session using credentials in secrets.json.

    :param aq_instance: the instance of Aquarium to use
        Corresponds to a key in the secrets.json file
    :type aq_instance: str
    :return: new Session
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'secrets.json')

    with open(filename) as f:
        secrets = json.load(f)

    credentials = secrets[aq_instance]
    session = AqSession(
        credentials["login"],
        credentials["password"],
        credentials["aquarium_url"]
    )

    msg = "Connected to Aquarium at {} using pydent version {}"
    print(msg.format(session.url, str(__version__)))

    me = session.User.where({'login': credentials['login']})[0]
    print('Logged in as {}\n'.format(me.name))

    return session

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def find_in_batches(model, ids, batch_size):
    n_total = len(ids)
    results = []
    nested_ids = chunks(ids, batch_size)

    for these_ids in nested_ids:
        these_results = model.where({"id": these_ids})
        if these_results:
            results += these_results
            n_found = len(results)
            pct_found = round((100 * n_found / n_total))
            print("Found {}% ({}) of {} records".format(pct_found, n_found, n_total))

    return results
