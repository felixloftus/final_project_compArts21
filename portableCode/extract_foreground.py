# ----------------------------------------------


# this code take an image path as an argument and runs a foreground subtraction on it
# based on the code here:
# https://debuggercafe.com/image-foreground-extraction-using-opencv-contour-detection/


# ----------------------------------------------


import numpy as np
import cv2
import argparse
import serial
import imutils
import os

#-----------------------------------------------------
#    This function finds all the contours in an image and returns the largest
#    contour area.
#-------------------

def find_largest_contour(image, min_area):

    # add min area here
    image = image.astype(np.uint8)
    # contours, hierarchy
    (_, cnts, _) = cv2.findContours(
        image,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        # areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > min_area:
            largest_contour = max(cnts, key=cv2.contourArea)
            return largest_contour

#-----------------------------------------------------
#   This function takes as arguments an image path, two thresholds, a minimum contour area, and an output path 
#   It does foreground extraction by creating a contour image using Canny Edge Detection and then using the contour image as a mask to crop the original image
#   https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
#-------------------

def extract_foreground_from_frame(input_file_path, threshold1, threshold2, min_area, output_folder_path):

    image = cv2.imread(input_file_path)

    # this section creates the contour image

    # blur the image to smmooth out the edges a bit, also reduces a bit of noise
    imgBlur = cv2.GaussianBlur(image, (5, 5), 0)
    # convert the image to grayscale 
    gray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    imgCanny = cv2.Canny(gray, threshold1, threshold2)
    kernel = np.ones((5,5))

    imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)
    contour = find_largest_contour(imgDil, min_area)

    image_contour = np.copy(image)
    cv2.drawContours(image_contour, [contour], 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)

    # this section uses the contour image as a mask for the original image and then saves the masked image and the contoured image

    # create a black 'mask' the same size as the original grayscale image 
    mask = np.zeros_like(gray)
    # fill the new mask with the shape of the largest contour
    # all the pixels inside that area will be white 
    cv2.fillPoly(mask, [contour], 255)
    # create a copy of the current mask
    res_mask = np.copy(mask)
    res_mask[mask == 0] = cv2.GC_BGD # obvious background pixels
    res_mask[mask == 255] = cv2.GC_PR_BGD # probable background pixels
    res_mask[mask == 255] = cv2.GC_FGD # obvious foreground pixels

    # create a mask for obvious and probable foreground pixels
    # all the obvious foreground pixels will be white and...
    # ... all the probable foreground pixels will be black
    mask2 = np.where(
        (res_mask == cv2.GC_FGD) | (res_mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype('uint8')


    # create 'new_mask3d' from 'mask2' but with 3 dimensions instead of 2
    new_mask3d = np.repeat(mask2[:, :, np.newaxis], 3, axis=2)
    mask3d = new_mask3d
    mask3d[new_mask3d > 0] = 255.0
    mask3d[mask3d > 255] = 255.0
    # apply Gaussian blurring to smoothen out the edges a bit
    # 'mask3d' is the final foreground mask (not extracted foreground image)
    mask3d = cv2.GaussianBlur(mask3d, (5, 5), 0)
    # show('Foreground mask', mask3d)

    # create the foreground image by zeroing out the pixels where 'mask2'...
    # ... has black pixels
    foreground = np.copy(image).astype(float)
    foreground[mask2 == 0] = 0
    cv2.imshow('Foreground', foreground.astype(np.uint8))

    # Save the images to the output folder
    save_name = os.path.basename(input_file_path).strip(".png")
    print(save_name)
    cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground.png"), foreground)
    cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground_mask.png"), mask3d)


