# -- coding: utf-8 --
import json


def read_json(file_name):
    json_file = '../test_data/json_data/' + file_name
    with open(json_file, 'r') as f:
        return json.loads(f.read())






