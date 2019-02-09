import numpy as np
import math
# convert_to_asc function found on image white points and converting then to 3D real points,
# by math equation with Calibrations Coefs and write it to asc file
# zaxis it is a motor step or step of scanner
# convert_to_asc return 3D points ONLY FROM ONE IMAGE, it means that you must call function n-times,where n is number of images.


def convert_to_asc(image, a_x, a_y, zaxis):
    # find points on image
    white_points_list_u = np.where(image == True)[1]
    white_points_list_v = np.where(image == True)[0]
    # print(white_points_list_v)
    worldZ = zaxis
    n = len(white_points_list_v)
    print(n)
    # throught all poitns create polinomal equation and use coefs and write to file
    result = []
    for i in range(0,n):
        cx = white_points_list_u[i]
        cy = white_points_list_v[i]
        pix = np.array([1, cx, cy, cx*cx, cx*cy, cy*cy])
        # print(pix)
        worldX = np.dot(pix, a_x)
        worldY = np.dot(pix, a_y)
        # print(worldX, worldY)
        # point = [*list(worldX), *list(worldY), worldZ*10]
        point = [worldX, worldY, worldZ*10]
        point = ["%.9f" % coord for coord in point]

        result.append(point)
    # print(result)
    return result
