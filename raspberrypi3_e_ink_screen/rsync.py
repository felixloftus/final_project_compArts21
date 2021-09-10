# ----------------------------------------------

# This file rsyncs the shared folder using the ip address of the camera
# This is achieved via SSH-ing into the rpi4 with a shared ssh-key
# https://www.raspberrypi.org/documentation/computers/remote-access.html#passwordless-ssh-access

# ----------------------------------------------
import os
import time

def sync_the_folder(rpi4_ip_address):
	os.system('rsync -avz -ssh pi@'+str(rpi4_ip_address)+':marksMade/output/ output/' )
	time.sleep(5)
	os.system('exit')