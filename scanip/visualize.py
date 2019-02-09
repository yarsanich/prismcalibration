from typing import Union

import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np


def display_points(points: Union[np.array, list]):
    x ,y = list(), list()
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, 'ro')
    plt.show()
