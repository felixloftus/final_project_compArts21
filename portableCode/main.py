# ----------------------------------------------


# This is a main program - It is designed for using to take computationally processed photographs
# The program either utilises the 'gathering.py' script which is used for gathering more images or the 'post_processing.py' is used for processing the images
# In this file, the program checks whether photos have already been taken, if they haven't then it moves to the 'gathering' phase
# If photos have been taken they the user is given an option whether to gather photos of process the photos


# ----------------------------------------------

#-----------------------------------------------------
# import the files necessary for processing the images
#-------------------

import sys
import os
from os import path
from gpiozero import Button
import time 
import cv2

#-----------------------------------------------------
# import the files necessary for processing the images
#-------------------

import gather
import post_processing

#-----------------------------------------------------
# variables 
#-------------------

button = Button(17)
button2 = Button(22)
button3 = Button(23)
button4 = Button(27)

UI_img1 = cv2.imread("UI/script2.png")
UI_img2 = cv2.imread("UI/script3.png")
UI_img3 = cv2.imread("UI/script4.png")

def check_folder_exists(dir_path, folder_str):
	return os.path.isdir(os.path.join(dir_path, folder_str))

#-----------------------------------------------------
# this function calls the 'gather' file which utilises the camera
#-------------------

def gather_session_movies(current_session_dir):
	video_folder = 'input_movies'
	video_folder_path = os.path.join(current_session_dir, video_folder) # a new folder is created for each 'session' of photographs
	os.makedirs(video_folder_path)
	gather.gather_session_movies(video_folder_path, button, button2, button3, button4)

#-----------------------------------------------------
# this function calls the 'gather' file which utilises the camera
#-------------------

def post_process_movie(session_path):
	## 1. convert videos to frames
	videos_to_frames_path = os.path.join(session_path, 'videos_to_images')
	if not os.path.exists(videos_to_frames_path):
		os.makedirs(videos_to_frames_path)
	# this is just copy and pasted from the code in the gather_session_movies function but should be taken via code
	# need to also check is current_session_dir is the same as session path?
	video_folder = 'input_movies'
	video_folder_path = os.path.join(session_path, video_folder)

	post_processing.videos_to_frames(video_folder_path, videos_to_frames_path)

	## 2. extract foregrounds from frames
	extract_foreground_output_path = os.path.join(session_path, 'extract_foreground_output')
	if not os.path.exists(extract_foreground_output_path):
		os.makedirs(extract_foreground_output_path)
	post_processing.extract_foreground_from_frames(videos_to_frames_path, extract_foreground_output_path, video_folder_path)

#-----------------------------------------------------
# main loop
#-------------------

if __name__=='__main__':

	dir_path = os.path.dirname(os.path.realpath('main.py'))

	while True:

		# For first time users it goes straight to taking the videos
		if not check_folder_exists(dir_path, "session_1"):
			print("Welcome new user, let's start taking photos")
			current_session_dir = os.path.join(dir_path, "session_1")
			os.makedirs(current_session_dir)
			gather_session_movies(current_session_dir)

		else:

			print("*****Main menu******\n\nWould you like to \n(1) take more movies\n(2) move to post processing? \n(3) exit\n(Please enter 1, 2 or 3)\n\n") # used for testing via SSH


			if button.is_pressed:
				print("\nTaking more movies...\n")
				existing_session_folders = [x for x in os.listdir() if x.startswith("session_")]

				max_existing_session = max([int(x.strip("session_")) for x in existing_session_folders])

				current_session_dir = os.path.join(dir_path, "session_{}".format(max_existing_session + 1))
				if not os.path.exists(current_session_dir):
					os.makedirs(current_session_dir)
				
				gather_session_movies(current_session_dir)
				print("Finished taking videos\n")

			elif button2.is_pressed:
				print("\nMoving to post_processing...\n")

				session_dirs = [x for x in os.listdir() if x.startswith("session_")]
				session_dir_paths = [os.path.join(dir_path, x) for x in session_dirs]

				for session_path in session_dir_paths:
					if (check_folder_exists(session_path, "input_movies")):
						# if (len(os.listdir(os.path.join(session_path, "input_movies"))) > 0) and (not check_folder_exists(session_path, "movies_to_frames")):
						if (len(os.listdir(os.path.join(session_path, "input_movies"))) > 0):
							post_process_movie(session_path)

			# Input val == '3' for exiting
			elif button3.is_pressed:
				print("Exiting...")
				break

			else:
				print("\nDidn't recognise that input, please try again\n")

