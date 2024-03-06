
import core.utils as utils
import streamlit as st
import pandas as pd
import tempfile
import cv2



DEMO_VIDEO = 'train.mp4'

st.title('Sign Language Letter Translator')
st.text("hello ")
st.sidebar.title('Choose options')

use_webcam = st.sidebar.button('Use webcam')
upload_file = st.sidebar.file_uploader('Upload a Image or Video', type=['mp4', 'jpg', 'png', 'jpeg'])

confidence_threshold = st.sidebar.slider('Confidence threshold', 0.0, 1.0, 0.5, 0.05)   

tfflie = tempfile.NamedTemporaryFile(delete=False)

if not upload_file:
    if use_webcam:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture(DEMO_VIDEO)
        tfflie.name = DEMO_VIDEO
else:
    tfflie.write(upload_file.read())
    

vid = cv2.VideoCapture(tfflie.name)
class_names = utils.read_class_names(cfg.YOLO.CLASSES)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.header('File preview')
    df = pd.read_csv(uploaded_file)
    st.write(df.describe())

    st.header('Data header')
    st.write(df.head())