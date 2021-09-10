# ----------------------------------------------


# This is the main file for /marksMade/stainedLand/*.png
# This file controls the Raspberry Pi Camera which is on a motorised slider
# The camera is performing a frame difference loop which builds up over time 
# The program creates 3 images in each loop which are saved in a folder shared with the screen raspberry pi
# Process:
# The program calls the gather function to take an image
# Then the image is contoured using edge detection
# Then the image is framedifferenced with the previous image
# Then the image is resized and saved in a shared folder
# The program then sends a message to the ESP driven Motor to tell the motor to move the camera
# The program then waits for a message from the motor before it takes a new photo
# Every three photos that are taken, the program sends a message to the Raspberry Pi powered e-ink screen to reload the screen with the new batch of images


# ----------------------------------------------

#-----------------------------------------------------
# import the necessary libraries
#-------------------
import sys
import os
from os import path
import time 
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from osc4py3 import oscmethod as osm

#-----------------------------------------------------
# import the files necessary for processing the images
#-------------------

import gather # gathers a 'raw' photograph
import contour # contour traces photograph
import frameDiff # 
import resizeImages

#-----------------------------------------------------
# variables 
#-------------------

global input_position
global loop_number
global osc_received
global image_counter
global frame_diff_counter
global last_deleted

last_deleted=1
loop_number=0
input_position=1
osc_received=False
msg=0
stored_exception=None
image_counter=1
frame_diff_counter=1

#-----------------------------------------------------
# OSC Setup
#-------------------

rpi4_ip_home = "192.168.0.80" 
rpi4_ip_Fefes_Wifi = "192.168.8.126 "
rpi4_ip = rpi4_ip_Fefes_Wifi

rpi3_ip_home = "192.168.0.119"
rpi3_ip_Fefes_Wifi = "192.168.8.237"
rpi3_ip = rpi3_ip_Fefes_Wifi

esp_ip_home = "192.168.0.102"
esp_ip_Fefes_Wifi = "192.168.8.124"
esp_ip = esp_ip_Fefes_Wifi
port = 8002
esp_port = 8006


#--------------------------------------------------------------------------------------
#----------------------------------------
# initialising functions 

#-----------------------------------------------------
# create necessary folders if they don't exist
#-------------------
def make_folders(dir_path):
    for x in range(1,4):
        contour_directories = os.path.join(dir_path, 'contoured', str(x))
        if not os.path.exists(contour_directories):
            os.makedirs(contour_directories)
        frameDiff_directories = os.path.join(dir_path, 'frameDiff', str(x))
        if not os.path.exists(frameDiff_directories):
            os.makedirs(frameDiff_directories)
        raw_directories = os.path.join(dir_path, 'raw', str(x))
        if not os.path.exists(raw_directories):
            os.makedirs(raw_directories)
        extracted_directories = os.path.join(dir_path, 'extracted', str(x))
        if not os.path.exists(extracted_directories):
            os.makedirs(extracted_directories)

#-----------------------------------------------------
# Initial loop that builds up the first set of images 
# for frame differencing
#------------------- 

def initial_loop(dir_path, extracted_or_not):
    global input_position
    global image_counter
    global frame_diff_counter
    
    # taken an image, contour it, then send a message to the ESP to move the camera along the slide clockwise
    # do this three times and then do the same anticlockwise
    for x in range(1, 4):   
        print("the input position is\n\n"+str(input_position))
        gather.gather_image(input_position, dir_path, image_counter)
        contour.contour_image(input_position, dir_path, image_counter, 'raw')
        input_position=input_position+1
        send_osc_esp()

    print("\n Now we have gathered three images and contoured them all ")
    image_counter=image_counter+1

    for x in range(3, 0, -1):   
        gather.gather_image(x, dir_path, image_counter)
        contour.contour_image(x, dir_path, image_counter, 'raw')
        input_position=input_position-1
        send_osc_esp()

    print('\n\nWe have finished second set of photos and contours\n\n')
    print('input_position is:')
    print(input_position)
    print('\n\n')
    image_counter=image_counter+1
    print('image_counter is:')
    print(image_counter)

    # now we have three sets of image 'pairs'
    # next, perform frame differencing on the image pairs and save the images in the frameDiff folder
    for x in range(1, 4):   
        print('\n\nDoing Frame Differencing and resizing on first set of photos:\n\n')
        frameDiff.frame_difference(dir_path, 'contoured', 'contoured', x, 1, 2, 1)
        resizeImages.resize_the_image(dir_path, x, frame_diff_counter)
    print('\n\nFrame Differencing and resizing now done \n\n onto sending to rpi3')
    frame_diff_counter=frame_diff_counter+1
    print('frame_diff_counter is:')
    print(frame_diff_counter)

    # now tell the e-ink screen to refresh its image
    send_osc_messages_rpi3(frame_diff_counter)

#--------------------------------------------------------------------------------------
#----------------------------------------
# Core functions 

#-----------------------------------------------------
# Core loop when camera is moving horizontally to the right
#------------------- 

def negative_core_loop(dir_path, extracted_or_not):
    global input_position
    global image_counter
    print('\nNow we do a negative core loop\n\n')
    print('image_counter is:')
    print(image_counter)

    # this counts down from three for the three positions the camera moves to

    for x in range(3, 0, -1):

        time.sleep(5)
        gather.gather_image(x, dir_path, image_counter)
        contour.contour_image(x, dir_path, image_counter, 'raw')

        # decrease input position - if it reaches 0 then the function breaks 

        input_position=input_position-1

        # tell ESP (which powers motor) to move the camera along

        send_osc_esp()

#-----------------------------------------------------
# Core functions when camera is moving horizontally to the left
#------------------- 

def positive_core_loop(dir_path, extracted_or_not):
    global input_position
    global image_counter

    input_position=1

    print('\nNow we do a positive core loop\n\n')
    print('image_counter is:')
    print(image_counter)

    # this counts up to three for the three positions the camera moves to
    for x in range(1, 4):

        time.sleep(5)
        gather.gather_image(input_position, dir_path, image_counter)
        contour.contour_image(input_position, dir_path, image_counter, 'raw')

        # increase input position - if it reaches 4 then the function breaks 

        input_position=input_position+1

        # tell ESP (which powers motor) to move the camera along

        send_osc_esp()

#-----------------------------------------------------
# This function removes old files left over from the previous use of this program
#------------------- 

def remove_directories(dir_path, image_counter):
    global last_deleted
    contour_directories = os.path.join(dir_path, 'contoured')
    frameDiff_directories = os.path.join(dir_path, 'frameDiff')
    raw_directories = os.path.join(dir_path, 'raw')
    print('\n\nRemoving Directories')
    for x in range(1,4):
        for y in range(last_deleted, image_counter-4):
            contour_image_file = os.path.join(contour_directories, str(x), str(y)+'.jpg')
            raw_image_file = os.path.join(raw_directories, str(x), str(y)+'.jpg')
            frameDiff_image_file = os.path.join(frameDiff_directories, str(x), str(y))+'.jpg'
            os.remove(contour_image_file) 
            os.remove(raw_image_file)
            os.remove(frameDiff_image_file)
    last_deleted=image_counter-4


#--------------------------------------------------------------------------------------
#----------------------------------------
# OSC

#-----------------------------------------------------
# receive messages
#-------------------
def handlerfunction(address, s):
    global msg
    print('this worked')
    msg=s
    print(msg)
    # Will receive message address, and message data flattened in s, x, y
    return

#-----------------------------------------------------
# send an osc message to the Raspberry Pi Screen 
#-------------------

def send_osc_messages_rpi3(frame_diff_counter):
    global input_position
    # this causes the Raspberry Pi Screen to reload the shared folder by ssh-ing into the Raspberry Pi Camera
    msg2 = oscbuildparse.OSCMessage("/update_ur_screen/", None, [str(frame_diff_counter)])
    osc_send(msg2, "rpi3")
    print('sent message to rpi3')
    input_position=0
    print(input_position)

#-----------------------------------------------------
# send an osc message to the ESP to move the camera along the slider and wait for the response that the slider has moved
#-------------------
def send_osc_esp():
    msg3 = oscbuildparse.OSCMessage("/move_me/", None, [1])
    # time.sleep(3)
    osc_send(msg3, "esp")
    print('sent message to esp')
    osc_process()
    continue_program=False;
    while True:
        starting_time = time.time()
        osc_process()
        while True:
            if time.time() - starting_time >= 1: #  a second or more
                break
            if msg==1:
                continue_program = True
        if continue_program:
            break
    msg = 0




#--------------------------------------------------------------------------------------
#----------------------------------------
# core loop

if __name__=='__main__':
    os.system("export DISPLAY=:0") # in case run on a remote computer via ssh

    print('\n\nWelcome to the show\n\n')

    dir_path = os.path.dirname(os.path.realpath('main.py')) # initialise main directory path - used for creating folders

    make_folders(dir_path) # create necessary folders if they do not exist

    osc_startup() # intialise the OSC for sending and receiving OSC messages 
    print('osc started up') # print to console for testing 

    osc_udp_client(rpi3_ip, port, "rpi3") # sending to screen channel
    osc_udp_client(esp_ip, esp_port, "esp") # sending to motor channel
    osc_udp_server(rpi4_ip, 8001, "camera") # setup port for listening
    print('osc_ud_server started up')

    osc_method("/test/", handlerfunction, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK) # listen for messages

    print('Now to do the initial loop: we take 3 photos then change direction and take another three')
    print('this loop should give us our first frame difference image')

    initial_loop(dir_path, True) # do initial loop for taking first set of photos - 
    # this loop needs to be different to the core loops because the core loop builds on existing edited photos
    # at the start there are no edited photos

    # each loop a new session is made
    try:
        while True:

            if image_counter%2==0:    
                # if image counter is even then we are moving to the right 
                negative_core_loop(dir_path, False)
            else:
                # if image counter is odd then we are moving to the left 
                positive_core_loop(dir_path, False)

            image_counter=image_counter+1 # increase the image counter each loop

            # for all 3 images taken in one of the core loops
            for x in range(1, 4): 

                # process the photos to create a frame differenced image and a resized image (for the e-ink screen)

                print('\n\nDoing Frame Differencing and resizing on new set of photos:\n\n')
                print('frame_diff_counter is: '+str(frame_diff_counter))

                if image_counter%50==0:

                    # this slows the build up to avoid too dense photographs 

                    frameDiff.frame_difference(dir_path, 'contoured', 'contoured', x, frame_diff_counter-1, image_counter-1, frame_diff_counter)
                else:

                    # this frame differences the images 

                    frameDiff.frame_difference(dir_path, 'frameDiff', 'contoured', x, frame_diff_counter-1, image_counter-1, frame_diff_counter)

                # this resizes the image and saves it to the shared folder 

                resizeImages.resize_the_image(dir_path, x, frame_diff_counter)

            print('\n\nFrame Differencing and resizing now done \n\n onto sending to rpi3')

            frame_diff_counter=frame_diff_counter+1

            print('frame_diff_counter is:')
            print(frame_diff_counter)

            send_osc_messages_rpi3(frame_diff_counter)

            osc_process()

            # this avoids the hard drive of the Raspberry Pi getting too full

            if image_counter>5:       
              remove_directories(dir_path, image_counter)

            # function to help stop the program
            if stored_exception:
                break

    except KeyboardInterrupt:
        print("[CTRL+C detected]")
        stored_exception=sys.exc_info()


# close off everything to clean up exit

osc_terminate()
sys.exit()







