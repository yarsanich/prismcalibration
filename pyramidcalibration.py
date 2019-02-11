from typing import List, NamedTuple, Union

import numpy as np

from imageprocessing import process_image
from scanip.image_proc import load_image
from scanip.visualize import display_points
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
        relations[str(points[point_index])] = (round((point_index * distance_btw_pixels) - 0.35 * LINE_LENGTH, 4), y)
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
    for point_index in range(points_num):
        point = Point(points[1][point_index], points[0][point_index]) # XXX TODO Move Upper
        try:
            real_coords = relations[str(point)]
            print("Found point {} with relation {}".format(point, relations[str(point)]))
            real_point = Point(real_coords[0], real_coords[1])
            real_points.append(real_point)
        except KeyError:
            print("Point is missing {}".format(point))
            continue
    return real_points


def filter_points(points, left_limit, right_limit) -> list:
    """
    :param points: points from image
    :param left_limit: left limit value of x imagine coordinate
    :param right_limit: right limit value of x imagine coordinate

    Return points with x coordinate between **left_limit** and
    **right_limit**.
    """
    filtered_points = list()
    for point in points:
        if left_limit <= point.x <= right_limit:
            filtered_points.append(point)
    return filtered_points


def update_relation(relations, newcome):
    '''
    :param relations:
    :param newcome:
    :return:
    '''
    for relation in newcome:
        if relation in relations:
            # new_relation = newcome[relation]
            # relations.update({relation: ((new_relation[0] + relations[relation][0]) / 2,
            #                              (new_relation[1] + relations[relation][1]) / 2)})
            relations.update({relation: newcome[relation]})
        else:
            relations.update({relation: newcome[relation]})

    return relations


def set_from_nparray(points):
    new_points = []
    for point_index in range(len(points[0]) - 1, 0, -1):
        new_points.append(Point(points[1][point_index], points[0][point_index]))
    return new_points


if __name__ == "__main__":
    import os

    y: Union[int, float] = 47.5
    y_step: Union[int, float] = 19 / 44

    os.chdir('captures/camera_1')
    images = sorted(os.listdir('.'))

    relations: dict = dict()
    for index, image in enumerate(images):
        current_index = index
        image = load_image(image)
        image[:, 0:428] = 0
        image[:, 713:] = 0
        points = process_image(image)
        points = np.where(points == True)
        points = set_from_nparray(points)
        points = filter_points(points, 428, 713) # for camera 1
        # points = filter_points(points, 660, 800)  # for camera 3
        try:
            new_relations = line_trans_relations(points, y)
            relations = update_relation(relations, new_relations)
        except ZeroDivisionError:
            pass
        y = round(y + y_step, 3)

    save_relations_to_yaml(relations, "../../relations_4")
    display_points(relations.values())
