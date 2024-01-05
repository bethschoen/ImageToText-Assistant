## IMAGE TO TEXT ASSISSTANT ##
# Author: Bethany Schoen
# Date: 5th January 2024
##############################
# To extract text from images 
# and provide summary info
# with a basic front end
##############################
# FRONT END CODE

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd

import image_to_text as itt

# page design

st.set_page_config(page_title="ImageToText Assisstant")

with st.sidebar:
    st.header('ImageToText Assisstant')
    st.subheader('Extract text from your images.')
    st.markdown('''
    # About
    I'm your digital text-extraction wizard! Drag and drop your text-packed images, and I'll work my magic, 
    turning them into editable text in a snap. Say goodbye to image-related headaches 👋 
    ''')
    add_vertical_space(2)
    st.write('Made with ❤️ by Beth')

# save session information
if 'image_info' not in st.session_state:
    st.session_state['image_info'] = []

upload = st.file_uploader("Please upload one or more images.", type=["png", "jpg"], accept_multiple_files=True)

if upload is not None:
    n_images = len(upload)
    for i, image in enumerate(upload):
        #bytes_data = image.getvalue()
        #st.write(bytes_data)
        extracted_text = itt.extract_text_from_image(i, image)
        print(extracted_text)
        word_count, char_count, char_count_no_spaces = itt.calculate_word_and_char_count(extracted_text)
        image_dict = {
            "Extracted Text":extracted_text,
            "Word Count":word_count,
            "Character Count":char_count,
            "Character Count (No Spaces)":char_count_no_spaces
        }

        st.session_state["image_info"].append({i:image, "info":image_dict})
        image_df = pd.DataFrame.from_dict(image_dict, orient='index', columns=["Image Info"])

        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image)

        with col2:
            st.table(image_df)