import json


def load(path):
    with open(path, 'r') as f:
        data = f.read()
    return json.loads(data)
