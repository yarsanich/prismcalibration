import json
import yaml
import numpy as np

def save_relations_to_json(relations: dict):
    with open('relations.json', 'w') as relations_file:
        json.dump(relations, relations_file)


def save_relations_to_yaml(relations: dict, filename: str):
    with open(filename + '.yaml', 'w') as relations_file:
        yaml.dump(relations, relations_file)


def load_relations_from_yaml(filename: str) -> dict:
    with open(filename + '.yaml', 'r') as relations_file:
        return yaml.load(relations_file)

def save_pointscloud(points: np.array, index=0, mode='w'):
    with open("../97_5.asc", mode) as asc_f:
        for point in points:
            asc_f.write("{}, {}, {}".format(str(point[0]), str(point[1]), index) + '\n')