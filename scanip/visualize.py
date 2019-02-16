from typing import Union

import matplotlib

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np


def display_points_based_on_image(points: list):
    import matplotlib.pyplot as plt

    xx = list()
    yy = list()

    plt.figure(1)

    prev_relation = points[0]

    for index, relation in enumerate(points):
        xx.append(relation['point'][0])
        yy.append(relation['point'][1])

        if relation['image_path'] != prev_relation['image_path']:
            # change color
            plt.scatter(xx, yy)
            plt.axis([0, 150, 40, 60])
            plt.show()
            xx = list()
            yy = list()
        prev_relation = relation


def display_points(points: Union[np.array, list], stop_exec=False, color='r'):
    x, y = list(), list()
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, f'{color}o')
    plt.show(block=stop_exec)
