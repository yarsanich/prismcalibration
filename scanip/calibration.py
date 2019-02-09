import numpy as np


def calibrate(points_on_image, x_real, y_real):
    np.set_printoptions(suppress=True)
    pix = np.empty((0, 6), int)
    for x in points_on_image:
        row = np.array([1, x[0], x[1], x[0] * x[0], x[0] * x[1], x[1] * x[1]])
        pix = np.vstack((pix, row))
    pix_t = np.matrix(np.transpose(pix))
    pix = np.matrix(pix)
    x_real = np.matrix(np.transpose(x_real))
    y_real = np.matrix(np.transpose(y_real))
    multiple = pix @ pix_t
    inv = np.linalg.inv(multiple)
    res = pix_t @ inv
    a_x = np.transpose(res @ np.transpose(x_real))
    a_y = np.transpose(res @ np.transpose(y_real))
    return (a_x.tolist(), a_y.tolist())
