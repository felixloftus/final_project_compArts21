# ----------------------------------------------

# This file waits for an osc message and then use it as a trigger to refresh the rsync folder

# ----------------------------------------------

#-----------------------------------------------------
# import the libraries necessary for refreshing the e-ink screen
#-------------------
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import os
import sys

#-----------------------------------------------------
# Import the files needed for the program
#-------------------

import rsync
import reload_screen

#-----------------------------------------------------
# Variables
#-------------------

global msg
global loop_number

stored_exception=None

loop_number = 0
msg=0

#-----------------------------------------------------
# Variables for OSC
#-------------------

rpi4_ip_home = "192.168.0.80"
rpi4_ip_Fefes_Wifi = "192.168.8.126"
rpi4_ip = rpi4_ip_Fefes_Wifi
rpi3_ip_home = "192.168.0.119"
rpi3_ip_Fefes_Wifi = "192.168.8.237"
rpi3_ip = rpi3_ip_Fefes_Wifi
port_IN = 8002
path_IN = "/update_ur_screen"


#-----------------------------------------------------
# Function for Receiving OSC messages
#-------------------

def handlerfunction(address, s):
	global msg
	msg=int(s)
	print('receiving from rpi4'+str(msg))
    # the msg variable will be equal to the number of photos that have been taken by the camera
	return


#-----------------------------------------------------
# Core Loop
# waits for OSC message, then refreshes the shared folder via the 'rsync.py' file, then refreshes the screen via the 'reload_screen.py' file
#-------------------
if __name__ == "__main__":
	dir_path = os.path.dirname(os.path.realpath('main.py')) # initialise main path
	osc_startup()
	# Make server channels to receive packets.
	osc_udp_server(rpi3_ip, port_IN, "rpi3")
	print('osc_ud_server started up')
	osc_method("/update_ur_screen/", handlerfunction, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
	try:
		while True:
			osc_process() # update the OSC 
			if msg>loop_number:
				print('msg is:'+str(msg))
				rsync.sync_the_folder(rpi4_ip)
				reload_screen.reloading(dir_path, msg) # msg will be the number of the latest photo taken
				loop_number=msg
				print('loop_number is: '+str(loop_number))
			if stored_exception: # used for terminating program via SSH
				break
	except KeyboardInterrupt: # used for terminating program via SSH
		print("[CTRL+C detected]")
		stored_exception=sys.exc_info()

#-----------------------------------------------------
# Ensures a clean exit
#-------------------
osc_terminate()
sys.exit()

