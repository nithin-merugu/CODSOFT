import streamlit as st
import cv2
import numpy as np
from face_recognizer import FaceRecognizer

st.title("Face Detection and Recognition App")

# Initialize face recognizer
try:
    face_recognizer = FaceRecognizer()
except Exception as e:
    st.error(f"Error initializing FaceRecognizer: {str(e)}")
    st.stop()

# Sidebar for adding known faces
st.sidebar.header("Add Known Face")
name = st.sidebar.text_input("Name")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None and name:
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    if face_recognizer.add_face(image, name):
        st.sidebar.success(f"Added {name} to known faces!")
    else:
        st.sidebar.error("No face detected in the uploaded image. Please try another image.")

# Main app
st.header("Upload an image for face detection and recognition")
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
    
    # Detect and recognize faces
    faces, face_names = face_recognizer.recognize_faces(image)
    
    if len(faces) > 0:
        # Draw faces and names
        result_image = face_recognizer.draw_faces(image, faces, face_names)
        
        # Display the result
        st.image(result_image, channels="BGR", use_column_width=True)
        
        st.write(f"Number of faces detected: {len(faces)}")
        for name in set(face_names):
            st.write(f"Recognized: {name}")
    else:
        st.image(image, channels="BGR", use_column_width=True)
        st.write("No faces detected in the image.")

    if not face_recognizer.is_model_trained:
        st.warning("The face recognition model hasn't been trained yet. Please add some known faces using the sidebar.")

st.header("Webcam Face Detection and Recognition")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

while run:
    _, frame = camera.read()
    
    # Detect and recognize faces
    faces, face_names = face_recognizer.recognize_faces(frame)
    
    if len(faces) > 0:
        # Draw faces and names
        result_frame = face_recognizer.draw_faces(frame, faces, face_names)
    else:
        result_frame = frame
    
    FRAME_WINDOW.image(result_frame, channels="BGR")
else:
    st.write('Stopped')

if not face_recognizer.is_model_trained:
    st.warning("The face recognition model hasn't been trained yet. Please add some known faces using the sidebar.")