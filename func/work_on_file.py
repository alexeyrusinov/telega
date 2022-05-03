import json


def get_name_station(name_file, id_station):
    name_station = ''
    with open(name_file) as f:  # Read json file
        stations = json.load(f)
        for k, v in stations.items():
            if v == f'{id_station}':
                name_station = k
        return name_station
