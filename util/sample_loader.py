import os
import re
import glob

def load_all_in_path(session, path, archive_path):
    """Load all .txt files in the given path, and move the files to the archive path.

    :param session: a Pydent Session
    :type session: AqSession
    :param path: the path containing the files to be loaded
    :type path: str
    :param archive_path: the path to move the files to once they are loaded
    :type archive_path: str
    :return: samples that have been created, grouped by filename
    :rtype: dict
    """
    sample_type = session.SampleType.find_by_name("Specimen")
    object_type = session.ObjectType.find_by_name("Nasopharyngeal Swab")
    location = "Ingest"
    new_samples_by_filename = {}

    for file_path in glob.glob(os.path.join(path, "*.txt")):
        data = read_data(file_path)
        new_samples = load_samples_and_items(data, session, sample_type, object_type, location)
        filename = os.path.basename(file_path)
        new_samples_by_filename[filename] = new_samples
        os.rename(file_path, os.path.join(archive_path, filename))

    return new_samples_by_filename

def read_data(file_path):
    """Read the file at the given path and return a list of properly formatted attributes.

    :param file_path: the path to the file to load
    :type file_path: str
    :return: formatted attributes
    :rtype: list
    """
    with open(file_path) as f:
        sample_data = []
        lines = f.readlines()
        filename = os.path.basename(file_path)

        for line in lines:
            attr = format_attributes(filename, line)
            if attr: sample_data.append(attr)
    return sample_data

def format_attributes(filename, line):
    """Take a line from the input file, and, if it finds the expected information, return a
            dict of attributes.

    :param filename: the basename of the file the line comes from
    :type filename: str
    :param line: a line from the file
    :type line: str
    :return: sample attributes
    :rtype: dict
    """
    mtch = re.search(r"(\d{2})\s+([ABCDEFGH])\s+(.+)", line)
    if mtch:
        specimen_barcode = mtch.group(3)
        rack_location = mtch.group(2) + mtch.group(1)
        rack_barcode = get_rack_barcode(filename)
        return {
            "name": "{}_{}".format(rack_barcode, rack_location),
            "description": "Specimen imported from file {}".format(filename),
            "project": "Test",
            "Specimen Barcode": specimen_barcode,
            "Ingest Rack Barcode": rack_barcode,
            "Ingest Rack Location": rack_location
        }

def load_samples_and_items(sample_data, session, sample_type, object_type, location):
    """Create samples corresponding to the given attributes. Create an item for each sample.

    :param sample_data: a list of dicts containing sample attributes
    :type sample_data: list
    :param session: a Pydent Session
    :type session: AqSession
    :param sample_type: the SampleType of the samples to be loaded
    :type sample_type: SampleType
    :param object_type: the ObjectType of the items to create for the loaded samples
    :type object_type: ObjectType
    :param location: the initial location for the new items
    :type location: str
    :return: list of samples
    :rtype: list
    """
    new_samples = []

    for s in sample_data:
        s["sample_type"] = sample_type
        attr = {}
        for a in ["name", "sample_type", "description", "project"]:
          attr[a] = s.pop(a)
        attr["properties"] = s
        new_sample = session.Sample.new(**attr)
        new_sample.save()

        new_item = session.Item.new(
            sample=new_sample,
            object_type=object_type
        )
        new_item.save()
        new_item.move(location)

        new_samples.append(new_sample_dict(new_sample, new_item, object_type))

    print("Loaded {} Samples with Items".format(len(new_samples)))

    return new_samples

def new_sample_dict(sample, item, object_type):
    """Make a dict of the inventory objects.

    :param sample:
    :type sample: Sample
    :param item:
    :type item: Item
    :param object_type:
    :type object_type: ObjectType
    :return: dict of inventory objects
    :rtype: dict
    """
    return {
        "sample": sample,
        "container": object_type,
        "item": item
    }

def get_rack_barcode(filename):
    """Extract rack barcode from the filename.

    :param filename:
    :type filename: str
    :return: the barcode
    :rtype: str
    """
    return re.search(r"\d+-(\d+).txt", filename).group(1)