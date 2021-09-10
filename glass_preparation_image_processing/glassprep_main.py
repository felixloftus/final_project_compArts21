# ----------------------------------------------

# This file prepares images for them to be engraved onto glass
# It can be run on the command line via the command 'python3 glassprep_main.py -i <input folder>'

# ----------------------------------------------

#-----------------------------------------------------
# Import the files needed for the program
#-------------------
import sys
import os
from os import path
import argparse
import glob

#-----------------------------------------------------
# Import the edge detection file 
#-------------------
import edges
movieCount = 1

# define the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to the input folder',
                    required=True)
args = vars(parser.parse_args())

if __name__=='__main__':
	imagecount = 0
	dir_path = os.path.dirname(os.path.realpath('glassprep_main.py')) # initialise the file path to this file
	output_path = os.path.join(args['input'], 'edge_outputs') # create an output folder within the input folder
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	for image in glob.glob(os.path.join(args['input'],'*.png')):
		edges.do_edges(image, output_path, str(movieCount)) # contour trace every file in the folder and output them to the output folder
		print(image)
		movieCount = movieCount+1

