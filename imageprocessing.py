from math import sqrt

import numpy as np
from scipy.misc import imshow
from skimage.feature import canny
from skimage.filters import threshold_otsu
from skimage.transform import probabilistic_hough_line

from scanip.image_proc import load_image, remove_small_obj  # , convert_to_bw
from linearmath import (LineSection, Point, distance_between_two_lines)


def thresh_image(image):
    thresh = threshold_otsu(image)
    # binary image
    image = image >= thresh
    return image


def process_image(image, show_result=False, with_skeletonize=True):
    """
    1. Create binary image(convert to black & white)
    2. Remove small objects
    3. Skeletonize
    """

    bw_image = image >= 100

    bw_wo_small_image = remove_small_obj(bw_image, 500)

    image_threshold = np.array(bw_wo_small_image)
    h, w = image_threshold.shape
    weight_matrix = np.array((np.matrix(np.linspace(0, w - 1, w)).T * np.matrix(np.ones(h))).T)

    # Compute center of mass
    s = image_threshold.sum(axis=1)
    v = np.where(s > 0)[0]
    u = (weight_matrix * image_threshold).sum(axis=1)[v] / s[v]
    image_line = np.zeros_like(image_threshold)
    image_line[v, u.astype(int)] = 255.0

    if show_result:
        import matplotlib.pyplot as pyplot
        pyplot.imshow(image_line)
        pyplot.show(image_line.any())

    return image_line if with_skeletonize else image_threshold


def find_border_lines(image):
    lines = probabilistic_hough_line(image, threshold=10)
    line_sections = []
    for line in lines:
        line_section = LineSection.from_two_points(Point(line[0][0], line[0][1]),
                                                   Point(line[1][0], line[1][1]))
        print(line_section.parameters())
        line_sections.append(line_section)
    return line_sections


def combine_line_sections(line_sections: list):
    # sort line sections by distance to first line section
    # if they are on the same line, append to line_1, else to line_2
    line_1 = [line_sections[0]]
    line_2 = []
    for index in range(1, len(line_sections)):
        print(distance_between_two_lines(line_sections[0], line_sections[index]))
        if distance_between_two_lines(line_sections[0], line_sections[index]) == 0:
            line_1.append(line_sections[index])
        else:
            line_2.append(line_sections[index])
    print(line_1, line_2)


def length_of_line(line):
    return sqrt((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2)


if __name__ == "__main__":
    image = load_image("capture_for_processing_test.jpg")
    line_sections = find_border_lines(image)

    combine_line_sections(line_sections)
