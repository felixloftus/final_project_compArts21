# ----------------------------------------------


# file to contour trace and adjust the detail
# code is based on the tutorial series "Python for Microscopists" and uses the Scikit Image library
# https://github.com/bnsreenu/python_for_microscopists

# ----------------------------------------------

# start by importing relevant libraries 
import sys
from skimage.filters import meijering, sato, frangi, hessian, roberts, sobel, scharr, prewitt # currently Roberts has been selected but these are alternatives
from skimage import io 
from skimage import data, exposure, util
import numpy as np
import os
from os import path
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True # stops errors with file sizes being too big


def contour_image(input_position, dir_path, image_counter, input_folder):
	print('starting contour')
	image = os.path.join(dir_path, input_folder, str(input_position), str(image_counter)+'.jpg')
	print(str(image))
	img = io.imread( image, as_gray=True)
	edge_roberts = roberts(img) # contour detection using the Roberts Cross method - details can be found here: https://en.wikipedia.org/wiki/Roberts_cross 

	p2, p98 = np.percentile(edge_roberts, (2, 98)) # Contrast stretching
	img_rescale = exposure.rescale_intensity(edge_roberts, in_range=(p2, p98)) # rescale image based on contrast stretching - this draws the detail in images
	contrasted_inverted = util.invert(img_rescale) # invert image
	contour_directory = os.path.join(dir_path, 'contoured') # create a new path for the contour directory for saving the image
	if not os.path.exists(contour_directory):
		os.makedirs(contour_directory) # if the directory doesn't exist then make the directory
	output_path=os.path.join(contour_directory, str(input_position), str(image_counter)+'.jpg') # create path for the image 
	io.imsave(output_path, contrasted_inverted) # save image in the correct 'input position' directory, within the contour directory - name the image after the loop number