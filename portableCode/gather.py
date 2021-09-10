# ----------------------------------------------


# This is a script for gathering photographs on a Raspberry Pi camera with 4 buttons attached


# ----------------------------------------------


from gpiozero import Button
import os
import time
import picamera
import datetime
import subprocess
import cv2

stillCount=0
startB = 0
stopB = False

getthetime = time.strftime("%Y%m%d-%H%M%S")
img = cv2.imread("UI/script1.png")
screen_res = 1280, 680
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)
cv2.namedWindow('Resized Window', cv2.WINDOW_NORMAL)
#resize the window according to the screen resolution
cv2.resizeWindow('Resized Window', window_width, window_height)


# Called when button is briefly tapped.  Creates Prievew
def preview():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.start_preview()
        time.sleep(8)
        camera.stop_preview()
        camera.close()


# Called when button is briefly tapped.  Gathers a still photograph
def gather():
    with picamera.PiCamera() as camera:
        camera.resolution = (4056, 3040)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(str(getthetime)+'.jpg')

# Called when button is briefly tapped.  Gathers a video to be processed into a photograph via the 'post_processing.py' file
def videoF(input_file_path, now):
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.framerate = 10
        print('long video Starting')  
        camera.start_recording(os.path.join(input_file_path, str(now)+'.h264'))
        camera.start_preview()
        camera.wait_recording(4) # changing to 4 for testing - was 40
        camera.stop_recording()
        camera.stop_preview()
        print('long video taken') 

# Called when button is briefly tapped.  Gathers a video to be processed into a photograph via the 'post_processing.py' file
def alt():
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.framerate = 5
        camera.start_recording(str(now)+'.h264')
        camera.start_preview()
        camera.wait_recording(20)
        camera.stop_recording()
        camera.stop_preview()

# main function that listens for buttons to be touched 
def gather_session_movies(input_file_path, button, button2, button3, button4):
    time.sleep(0.05)
    while True:
        cv2.imshow('Resized Window', img)
        now = datetime.datetime.now()
        timestamp = now.strftime("%y%m%d%H%M%S")

        if button.is_pressed:
            preview()
            print("preview")

        if button2.is_pressed:
            gather()
            print("photo taken ")

        if button3.is_pressed:
            videoF(input_file_path, now)

        if button4.is_pressed: # button 4 breaks the loop to return to the 'main.py' file
            break

        if cv2.waitKey(1) == 27: # escape key exits for testing
            break 

    cv2.destroyAllWindows()
    return