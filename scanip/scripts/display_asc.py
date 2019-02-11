"""
    Script for display .asc 3D point data in RAW in (x, y, z) format
    Example usage:
    python display_asc.py ./test.asc
"""
import argparse
import numpy as np
from matplotlib import pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D


def read_data_from_file(filepath):
    """Read points from .asc file"""
    print("Get {}".format(filepath))
    # Get RAW DATA line by line
    with open(filepath, "r") as datafile:
        raw_data = [line[:-1] for line in datafile]

    # Parse ASC File for points
    points = [tuple(map(float, line.split(','))) for line in raw_data]
    return points


def plot_data_with_matplotlib(points: np.array):
    """Plot 3D points with matplotlib Axes3D"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(points[0], points[1], points[2], c='r', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
