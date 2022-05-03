import json


def load_file(file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
        stations = dict(reversed(list(stations.items())))  # revers
    return stations


def get_name_station(name_file, id_station):
    name_station = ''
    with open(name_file) as f:  # Read json file
        stations = json.load(f)
        for k, v in stations.items():
            if v == f'{id_station}':
                name_station = k
        return name_station


def get_station(value, file):
    with open(file) as f:  # Read json file
        stations = json.load(f)
    my_dict = {}
    for k, v in reversed(stations.items()):
        if value in k.upper():
            my_dict.update({k: v})
    return my_dict


