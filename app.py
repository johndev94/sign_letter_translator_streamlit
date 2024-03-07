# Python In-built packages
import os
from pathlib import Path
import PIL
import pandas as pd
# External packages
import streamlit as st

# Local Modules
import settings
import helper



# Setting page layout
st.set_page_config(
    page_title="Sign Language Letter Translator ",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"

)

# Main page heading
st.title("Sign Language Letter Translator")

# Sidebar
st.sidebar.header("Configuration")

language_from = st.sidebar.selectbox(
    "Select Language From",
    settings.LANGUAGES
)

# Filter out selected language from the list
languages_to = [lang for lang in settings.LANGUAGES if lang != language_from]

language_to = st.sidebar.selectbox(
    "Select Language to tranlate to",
    languages_to
)

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Translation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
# CHANGE THIS
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)
 
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
name = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    if source_img is None:
        # Display the default image in a single column spanning the width of 3 columns
        default_image_path = str(settings.DEFAULT_IMAGE)
        try:
            default_image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption="Welcome to the Sign Language Letter Translation App", use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)
    else:
        # Use a three-column layout when source_img is not None
        col1, col2, col3 = st.columns(3)

        with col1:
            try:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image", use_column_width=True)
            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)

    # Only display col2 and col3 if source_img is not None
    if source_img is not None:
        with col2:
            if source_img is None:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(
                    default_detected_image_path)
                st.image(default_detected_image_path, caption='Detected Image',
                        use_column_width=True)
            else:
                if st.sidebar.button('Detect Objects'):
                    res = model.predict(uploaded_image,
                                        conf=confidence
                                        )
                    boxes = res[0].boxes
                    
                    res_plotted = res[0].plot()[:, :, ::-1]

                    ## Gets all data from the detection
                    for result in res:

                        detection_count = result.boxes.shape[0]

                        for i in range(detection_count):
                            cls = int(result.boxes.cls[i].item())
                            name = result.names[cls]
                            confidence = float(result.boxes.conf[i].item())
                            bounding_box = result.boxes.xyxy[i].cpu().numpy()

                            x = int(bounding_box[0])
                            y = int(bounding_box[1])
                            width = int(bounding_box[2] - x)
                            height = int(bounding_box[3] - y)

                    print(name, confidence, x, y, width, height)


                    st.image(res_plotted, caption=f'Detected Letter: {name}',
                            use_column_width=True)
                    
                    

                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        # st.write(ex)
                        st.write("No image is uploaded yet!")

        with col3:
            if source_img is None:
                default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(default_detected_image_path, caption='Detected Image', use_column_width=True)
            else:
                if name:  # Checks if 'name' is not empty or None
                    # Constructs the file path for the corresponding translated letter image
                    translated_image_path = os.path.join("C:\\Users\\John\\Desktop\\Coding Projects\\Python\\sign_letter_translator_streamlit\\translated letters\\ISL", f"{name}.JPG")


                    
                    if os.path.exists(translated_image_path):  # Checks if the file exists
                        translated_image = PIL.Image.open(translated_image_path)
                        st.image(translated_image, caption=f'Translated Letter: {name}', use_column_width=True)
                    else:
                        st.write(f"No translated image found for letter: {name}")
                        print("Current Working Directory:", os.getcwd())
                        print(translated_image_path)
                else:
                    st.write("No letter detected or name variable is empty.")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

else:
    st.error("Please select a valid source type!")
