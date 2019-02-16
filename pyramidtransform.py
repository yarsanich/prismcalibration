import math
import random

import numpy as np

from utils import (
    load_relations_from_yaml,
    save_pointscloud
)
from pyramidcalibration import (
    transform_points,
    load_image,
)
from imageprocessing import process_image
from scanip.visualize import display_points, display_points_based_on_image


def transform_image(filename, relations):
    image = load_image(filename)

    image_points = process_image(image, True, True)

    image_points = np.where(image_points == True)

    return transform_points(image_points, relations)


if __name__ == "__main__":
    relations = load_relations_from_yaml('relations_temp')
    points = transform_image('./camera_2.jpg', relations)

    # relations_x = load_relations_from_yaml('relations_3')
    # points_x = transform_image('./camera_1.jpg', relations_x)

    display_points_based_on_image(points)

    # display_points(points)
    # display_points(points_x)
    # display_points(points + points_x)
