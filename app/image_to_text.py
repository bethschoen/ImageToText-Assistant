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
    img = Image.open(file).convert("RGB")
    img = np.array(img)
    #img = cv2.imread(img)
    cv2.imwrite(r"C:\Users\Beth\OneDrive - Amey plc\Documents\Be Digital\New folder\ImageToText-Assistant\app\uploaded_images\img_"+str(i)+".png", img)

    # process each image to make text more readable
    # convert to greyscale (has to be thresholding)
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Improve contrast (helps with light coloured text)
    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # Apply CLAHE
    clahe_image = clahe.apply(greyscale)
    # Convert to black and white
    ret, thresh = cv2.threshold(clahe_image, 127, 255, cv2.THRESH_BINARY)

    cv2.imwrite(r"C:\Users\Beth\OneDrive - Amey plc\Documents\Be Digital\New folder\ImageToText-Assistant\app\processed_images\img_"+str(i)+".png", clahe_image)
    image_text = pytesseract.image_to_string(clahe_image, config='--psm 11')# -c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ')

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

