import json
import os
from app import app


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def load_machine():
    return read_json(os.path.join(app.root_path, 'data/machine.json'))


def load_data(machine_id):
    path_js = 'data/'+machine_id+'.json'
    return read_json(os.path.join(app.root_path, path_js))
