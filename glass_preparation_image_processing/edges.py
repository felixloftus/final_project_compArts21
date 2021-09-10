# ----------------------------------------------


# This file does contour tracing with the Roberts Cross Algorithm
# it is based on the 'computer vision for microscopists tutorial'
# https://github.com/bnsreenu/python_for_microscopists


# ----------------------------------------------

from skimage.filters import meijering, sato, frangi, hessian, roberts, sobel, scharr, prewitt
from skimage import io
from skimage import data, exposure, util
import numpy as np
import os
from os import path
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def identity(image, **kwargs):
    """Return the original image, ignoring any kwargs."""
    return image

def do_edges(image, output_path, output_name):
	img = io.imread( image, as_gray=True)
	edge_roberts = roberts(img)

	# Contrast stretching
	p2, p98 = np.percentile(edge_roberts, (2, 98))
	img_rescale = exposure.rescale_intensity(edge_roberts, in_range=(p2, p98))
	contrasted_inverted = util.invert(img_rescale)
	io.imsave(os.path.join(output_path, f"{output_name}.png"), contrasted_inverted)

	# f"{save_name}_foreground.png"