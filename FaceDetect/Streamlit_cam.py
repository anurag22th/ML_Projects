import streamlit as st
import streamlit.components as components
import cv2
import logging as log
import datetime as dt
from time import sleep

casscPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(casscPath)
log.basicConfig(filename='webcam.log', level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

# strmlt

st.title("FaceDetect")

#sidebar
st.sidebar.subheader("Details")
t1 = st.sidebar.text_input("Name for person1")
s1 = st.sidebar.slider("Age for person1")

st.sidebar.markdown("----------")

t2 = st.sidebar.text_input("Name for person2")
s2 = st.sidebar.slider("Age for person2")

st.write("Name : ", t1)
st.write("Age : ", s1)
st.write("Name : ", t2)
st.write("Age : ", s2)

st.header("Face Detection")
if st.button("Can I detect your face ?"):
    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw rectangle around  faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

        # Display result frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Display result frame
        cv2.imshow('Video', frame)

#  release capture
video_capture.release()
cv2.destroyAllWindows()