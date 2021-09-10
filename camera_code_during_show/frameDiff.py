# ----------------------------------------------


# This function does framedifferencing based on two inputted images
# It is based on Scikit Image's method for visual image comparison
# https://scikit-image.org/docs/dev/auto_examples/applications/plot_image_comparison.html#sphx-glr-auto-examples-applications-plot-image-comparison-py


# ----------------------------------------------
# import relevant libraries 
from skimage import io
from skimage import data, transform, exposure
from skimage.util import compare_images
from PIL import ImageFile
import numpy as np
import os
from os import path
ImageFile.LOAD_TRUNCATED_IMAGES = True # used to stop errors with file size

# dir_path tells the function where to look for images
# img1/2_path are the paths of the images that will be compared 
# in the first loop both will be from the contoured folder
# after the first loop the first will be from the frame differenced folder and the second will be from the contoured folder
# the output path argument tells the function where to save the image
def frame_difference(dir_path, img1_path, img2_path, input_position, image_counter, image_counter2, output_path):
	image1_path = os.path.join(dir_path, img1_path, str(input_position), str(image_counter)+'.png')
	image2_path = os.path.join(dir_path, img2_path, str(input_position), str(image_counter2)+'.png')
	img1 = io.imread(image1_path, as_gray=True)
	img2 = io.imread(image2_path, as_gray=True)
	diff_photo = compare_images(img1, img2, method='diff')
	frameDiff_directory = os.path.join(dir_path, 'frameDiff')
	output_path=os.path.join(frameDiff_directory, str(input_position), str(output_path)+'.png')
	io.imsave(output_path, diff_photo)