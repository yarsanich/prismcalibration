from PIL import Image
import skimage.filters
import skimage.morphology
import numpy as np
import scipy.misc
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral
from scipy import ndimage as ndi


def load_image(filename):
    img = Image.open(filename)
    img = img.convert('L')
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


# Skimage skeletonize

def skeletonize(image):
    thr = skimage.filters.threshold_otsu(image)
    image = image>thr  # Threshold the image
    # skeletonize can take boolean list
    im_sk = skimage.morphology.skeletonize(image)
    return im_sk

#convert to black and white
#bw_coef is a breakpoint pixel. Greater bw_coef will be white, less will be black.
def convert_to_bw(image, bw_coef):
    image[image < bw_coef] = 0    # Black
    image[image >= bw_coef] = 255 # White
    return image

# remove_small_obj function remove from image small pieces of white pixels
# remove_coef setup size of it pieces
def remove_small_obj(image, remove_coef):
    label_objects, nb_labels = ndi.label(image)
    sizes = np.bincount(label_objects.ravel())
    mask_sizes = sizes > remove_coef  # 1000 for correct detect laserline
    mask_sizes[0] = 0
    im_cleaned = mask_sizes[label_objects]
    return im_cleaned
