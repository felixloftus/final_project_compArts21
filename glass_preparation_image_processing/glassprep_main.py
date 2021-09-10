import sys
import os
from os import path
from gpiozero import Button
import time 
import argparse
import glob

import edges
movieCount = 1

# define the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to the input folder',
                    required=True)
args = vars(parser.parse_args())

types = ('*.png', '*.jpg') # the tuple of file types
files_grabbed = []

if __name__=='__main__':
	imagecount = 0
	dir_path = os.path.dirname(os.path.realpath('glassprep_main.py'))
	output_path = os.path.join(args['input'], 'edge_outputs')
	if not os.path.exists(output_path):
		os.makedirs(output_path)
	for image in glob.glob(os.path.join(args['input'],'*.png')):
		edges.do_edges(image, output_path, str(movieCount))
		print(image)
		movieCount = movieCount+1

