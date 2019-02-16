from random import randint
from typing import List, NamedTuple, Union

import numpy as np

from imageprocessing import process_image
from scanip.image_proc import load_image
from scanip.visualize import display_points, display_points_based_on_image
from utils import (
    save_relations_to_yaml
)

np.set_printoptions(threshold=np.inf)

LINE_LENGTH: Union[int, float] = 160  # length of line in mm

current_index = 0


class Point(NamedTuple):
    x: int  # Ignore PEP8Bear
    y: int

    def __repr__(self):
        return str((self.x, self.y))

    def __str__(self):
        return str((self.x, self.y))


def line_trans_relations(points: List[Point], y: Union[int, float]) -> dict:
    """
    :param points: list of points(one line on pyramid)
    :param y: real y coordinate of line

    Calculate (x, y) real coordinates to every point from **points** and
    return dictionary with relations str(point): (x, y). (stringified point as
    key and tuple with real coordinates as value).
    """
    relations: dict = dict()
    points_num: int = len(points)

    distance_btw_pixels: float = round(LINE_LENGTH / points_num, 4)
    for point_index in range(points_num):
        relations[str(points[point_index])] = (round(point_index * distance_btw_pixels, 4), y)  # - 0.35 * LINE_LENGTH
    return relations


def transform_points(points: np.array, relations: dict) -> list:
    """
    :param points: np.array with points from image
    :param relations: relations between points on image and real coordinates

    Return list of real coordinates of points, that have representation in
    relations
    """
    points_num = len(points[0])
    real_points = []
    missing_points = []
    for point_index in range(points_num):
        point = Point(points[1][point_index], points[0][point_index])  # XXX TODO Move Upper
        try:
            real_coords = relations[str(point)]['point']
            image_path = relations[str(point)]['image_path']
            print("Found point {} with relation {}".format(point, relations[str(point)]))
            real_point = Point(real_coords[0], real_coords[1])
            real_points.append({'point': real_point, 'image_path': image_path})
        except KeyError:
            print("Point is missing {}".format(point))
            missing_points.append(point)
            continue

    print("Missing points Length", len(missing_points))
    display_points(missing_points, True)

    return real_points


def update_relation(relations, newcome, line_index, image_path: str = None):
    '''
    :param relations:
    :param newcome:
    :return:
    '''
    existing_points = []

    for relation in newcome:
        if relation in relations:
            new_relation = newcome[relation]
            point = ((new_relation[0] + relations[relation]['point'][0]) / 2,
                     (new_relation[1] + relations[relation]['point'][1]) / 2)
            print("Already exist", relation, newcome[relation], f"Line index {line_index}")
            existing_points.append(eval(relation))
            # relations.update({relation: newcome[relation]})
        else:
            point = newcome[relation]

        relations.update({relation: {
            'point': point,
            'image_path': image_path,
        }})

    # display_points(existing_points)

    return relations


def set_from_nparray(points):
    new_points = []
    for point_index in range(len(points[0]) - 1, 0, -1):
        new_points.append(Point(points[1][point_index], points[0][point_index]))
    return new_points


if __name__ == "__main__":
    import os

    y: Union[int, float] = 47.5
    y_start = 47.5
    y_step: Union[int, float] = 15 / 44

    camera_directory = 'captures/camera_1'

    os.chdir(camera_directory)
    images = sorted(os.listdir('.'))

    image_points = []

    relations: dict = dict()
    for index, image in enumerate(images):
        if index % 3 == 0:
            continue
        if image.startswith('proc'):
            break
        current_index = index

        image_name = image

        image = load_image(image)
        image[:, 0:428] = 0
        image[:, 713:] = 0
        points = process_image(image, False, False)
        points = np.where(points == True)
        points = set_from_nparray(points)
        points = list(filter(lambda x: 428 <= x.x <= 713, points))  # for camera 1
        # points = filter_points(points, 660, 800)  # for camera 3

        image_points = [*image_points, *points]

        try:
            new_relations = line_trans_relations(points, y)
            relations = update_relation(relations, new_relations, index, f'{camera_directory}/{image_name}')
        except ZeroDivisionError:
            pass
        y = round(y + y_step, 2)

    display_points(image_points, True)

    save_relations_to_yaml(relations, "../../relations_temp")

    sorted_relations = sorted(relations.values(), key=lambda x: x['image_path'])

    prev_relation = sorted_relations[0]

    display_points_based_on_image(sorted_relations)

# display_points([point['point'] for point in relations.values()], True)
