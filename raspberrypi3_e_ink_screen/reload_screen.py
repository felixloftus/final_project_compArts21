# ----------------------------------------------

# This file reloads the screen with three consecutive images and then turns of the screen
# This limits the amount of power drawn from the screen
# On e-ink screens the image remains on the screen even if the screen is off

# ----------------------------------------------

import logging
import time
from PIL import Image,ImageDraw,ImageFont, ImageOps
import traceback
import sys
import os

logging.basicConfig(level=logging.DEBUG)

def reloading(dir_path, msg):

    # for the screen it is necessary to point the program towards the screens libraries
    libdir = os.path.join(dir_path, 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)

    from waveshare_epd import epd5in83_V2
    try:
        # intialise the screen
        epd = epd5in83_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        
        logging.info("Read file")
        # this loads one image for each position on the slider, of which there are always three
        image1 = Image.open(os.path.join(dir_path, 'output', '1', str(msg-1)+'.jpg'))
        image2 = Image.open(os.path.join(dir_path, 'output', '2', str(msg-1)+'.jpg'))
        image3 = Image.open(os.path.join(dir_path, 'output', '3', str(msg-1)+'.jpg'))

        epd.display(epd.getbuffer(image1))
        time.sleep(2)
        epd.display(epd.getbuffer(image3))
        time.sleep(2)
        epd.display(epd.getbuffer(image2))
        time.sleep(2)
        
        logging.info("Clear...")
        
        logging.info("Goto Sleep...")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in83_V2.epdconfig.module_exit()
        exit()