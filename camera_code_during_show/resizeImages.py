# ----------------------------------------------


# This function resizes an image to the size necessary for the e-ink screen


# ----------------------------------------------

from PIL import Image
import os
from os import path

def resize_the_image(dir_path, input_position, frame_diff_counter):
	image_path = os.path.join(dir_path, 'frameDiff', str(input_position), str(frame_diff_counter)+'.png')
	img = Image.open(image_path)
	new_img = img.resize((648,480))
	output_path = os.path.join(dir_path, 'output', str(input_position), str(frame_diff_counter)+'.png')
	new_img.save(output_path, "PNG", optimize=True)