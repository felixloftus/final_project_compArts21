# ----------------------------------------------


# This is a script for processing photographs on a Raspberry Pi camera 
# it uses image segmentation, by extracting the foreground from an image.


# ----------------------------------------------

#-----------------------------------------------------
# import the libraries necessary for processing the images
#-------------------

import glob
import argparse
import os, random 
import time
import subprocess

#-----------------------------------------------------
# imports the 'extract_foreground.py' file
#-------------------

import extract_foreground

#-----------------------------------------------------
# variables 
#-------------------

global movieCount
global movieToImages

#-----------------------------------------------------
# function to split all videos into frames by using FFMPEG
#-------------------

def videos_to_frames(input_path, output_path):
    movieCount = 1
    for video in glob.glob(os.path.join(input_path,'*.h264')):
        video_frame_dir = os.path.join(output_path, str(movieCount))
        if not os.path.exists(video_frame_dir):
            os.makedirs(video_frame_dir)
        os.system('ffmpeg -i '+str(video)+' -vf fps=5 '+str(video_frame_dir)+'/%04d.png')
        print("Finished converting movie {} to frames".format(movieCount))
        movieCount = movieCount+1
    return 


#-----------------------------------------------------
# function to extract foreground from all movie files 
#-------------------

def extract_foreground_from_frames(movies_to_frames_dir_path, output_path, input_path):
    
    movieCount = 1  
    for video in glob.glob(os.path.join(input_path,'*.h264')): # this counts to check how many movies there are to process
        movieCount = movieCount+1

    for x in range(1,movieCount+1):

        extracted_movie_path = os.path.join(output_path, str(x)) # this makes a directory for each movie that has been gathered
        if not os.path.exists(extracted_movie_path):
            os.makedirs(extracted_movie_path)

        for frame in glob.glob(os.path.join(movies_to_frames_dir_path, str(x), '*.png')): # this extracts a foreground for each frame in each movie
            threshold1 = 10
            threshold2 = 20
            min_area = 30
            
            print(frame)
            for i in range(15): # value can be adjusted depending on version of Raspberry Pi - tested on a Raspberry Pi 4 and Raspberry Pi 3b+
                try: # attempts to extract foreground on each frame for a range of thresholds
                    extract_foreground.extract_foreground_from_frame(frame, threshold1, threshold2, min_area, extracted_movie_path)
                    break # if the extraction is succesful this loop breaks and the function ends
                except:
                    print("Extracting foreground threshold did not work...try new threshold")
                    threshold1 += 15
                    threshold2 += 15

