# ----------------------------------------------


# This file takes a photograph
# the camera then turns off once the function is no longer being called
# this ensures the camera is on for a minimal period
# this decision was made to reduce power consumption
# this is tested on both a HQ camera, and the V1 Raspberry Pi Cameras
# this is tested on both a raspberry pi 4 and a raspberry pi 3b+

# ----------------------------------------------

import os
from os import path
import picamera
import time

# input_number argument keeps track of what position along the slider the camera is
# dir_path leads to the director the main.py file is kept 
# the image_counter is used to name the image files captured
def gather_image(input_number, dir_path, image_counter):
    with picamera.PiCamera() as camera:
        camera.resolution = (2028, 1520)
        camera.brightness = (70)
        camera.contrast = (65)
        # camera.start_preview() # used for testing with screen attached
        print('image taken')
        time.sleep(2) # Camera warm-up time
        camera.capture(os.path.join(dir_path, 'raw', str(input_number), str(image_counter)+'.png'))
