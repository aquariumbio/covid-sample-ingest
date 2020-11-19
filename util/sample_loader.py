import csv

def load_samples_from_csv(file_path, session, st_name):
    with open(file_path) as csvfile:
        sample_data = csv.DictReader(csvfile)
        return load_samples(sample_data, session, st_name)

def load_samples(sample_data, session, st_name):
    sample_type_id = session.SampleType.find_by_name(st_name).id
    new_samples = []
    for s in sample_data:
        s["sample_type_id"] = sample_type_id

        attr = {}
        for a in ["name", "sample_type_id", "description", "project"]:
          attr[a] = s.pop(a)

        attr["properties"] = s

        new_sample = session.Sample.new(**attr)
        new_sample.save()
        new_samples.append(new_sample)

    print("Loaded {} Samples".format(len(new_samples)))

    return new_samples

def create_items(samples, session, ot_name, location):
    ot = session.ObjectType.find_by_name(ot_name)
    new_items = []
    for sample in samples:
        new_item = session.Item.new(
            sample_id=sample.id,
            object_type_id=ot.id
        )
        new_item.save()
        new_item.move(location)
        new_items.append(new_item)

    print("Created {} Items".format(len(new_items)))

    return new_items