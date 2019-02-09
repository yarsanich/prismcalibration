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


def plot_data_with_matplotlib(points):
    """Plot 3D points with matplotlib Axes3D"""
    fig = plt.figure(figsize=(7,5))
    ax = Axes3D(fig)

    x= np.array(list(map(lambda x: x[0], points)))
    y= np.array(list(map(lambda x: x[1], points)))
    z= np.array(list(map(lambda x: x[2], points)))
    
    ax.plot(x, y, z, 'ok')

    plt.show()


def main(filepath):
    """Get data from file, then plot with matplotlib"""
    points = read_data_from_file(filepath)
    plot_data_with_matplotlib(points)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="path to file with asc data")
    args = parser.parse_args()
    main(args.filepath)
