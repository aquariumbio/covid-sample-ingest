import os
import csv
import glob

def load_all_in_path(session, path, archive_path):
    new_samples_by_filename = {}
    for file_path in glob.glob(os.path.join(path, "*.csv")):
        new_samples = load_from_csv(file_path, session, "Specimen", "Nasopharyngeal Swab", "Ingest")
        filename = os.path.basename(file_path)
        new_samples_by_filename[filename] = new_samples
        os.rename(file_path, os.path.join(archive_path, filename))
    return new_samples_by_filename

def load_from_csv(file_path, session, st_name, ot_name, location):
    with open(file_path) as csvfile:
        sample_data = csv.DictReader(csvfile)
        return load_samples_and_items(sample_data, session, st_name, ot_name, location)

def load_samples_and_items(sample_data, session, st_name, ot_name, location):
    sample_type = session.SampleType.find_by_name(st_name)
    object_type = session.ObjectType.find_by_name(ot_name)
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
        new_samples.append(values(new_sample, new_item, object_type))

    print("Loaded {} Samples with Items".format(len(new_samples)))

    return new_samples

def values(sample, item, object_type):
    return {
        "sample": item.sample,
        "container": object_type,
        "item": item
    }