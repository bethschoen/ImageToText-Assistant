## IMAGE TO TEXT ASSISSTANT ##
# Author: Bethany Schoen
# Date: 5th January 2024
##############################
# To extract text from images 
# and provide summary info
# with a basic front end
##############################
# BACK END CODE

from PIL import Image
import pytesseract
import cv2
import re
import io
import numpy as np

import variables as vr

pytesseract.pytesseract.tesseract_cmd = vr.pytesseract_exe_location

def extract_text_from_image(i, file):
    """
    Given a file path, process the image at the file location and extract text
    """
    # save file locally
    img = Image.open(file) #io.BytesIO(file)
    img = np.array(img)
    #img = cv2.imread(img)
    # process each image to make text more readable
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noise = cv2.medianBlur(greyscale, 3)
    thresh = cv2.threshold(greyscale, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # Perform dilation and erosion to remove some noise 
    kernel = np.ones((1, 1), np.uint8) 
    dilate = cv2.dilate(greyscale, kernel, iterations=1) 
    erode = cv2.erode(dilate, kernel, iterations=1) 
    cv2.imwrite(r"C:\Users\Beth\OneDrive - Amey plc\Documents\Be Digital\New folder\ImageToText-Assistant\app\processed_images\img_"+str(i)+".png", thresh)

    image_text = pytesseract.image_to_string(thresh, config='--psm 12 --oem 3')# -c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ')

    # replace any white spaces with one space 
    image_text = re.sub(r'\s+', ' ', image_text)
    image_text = image_text.strip()

    return str(image_text)

def calculate_word_and_char_count(extracted_text):

    # tokenize by space and count words
    word_count = len(extracted_text.split(" "))
    # count characters
    char_count = len(extracted_text)
    # remove spaces and count characters
    char_count_no_spaces = len(extracted_text.replace(" ", ""))

    return str(word_count), str(char_count), str(char_count_no_spaces)

