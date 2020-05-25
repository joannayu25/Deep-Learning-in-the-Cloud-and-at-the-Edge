import cv2
import numpy as np
import paho.mqtt.client as mqtt

# Load the cascade
face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(1)

client = mqtt.Client()
client.connect('mosquitto')

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_gray = gray[y:y + h, x:x + w] 
        # Encode as binary message and send
        _, png = cv2.imencode('.png', face_gray)
        msg = png.tobytes()
        client.publish('face_detection_topic', msg, 0) 

    # Display
    cv2.imshow('img', img)
  

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
        
# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
client.disconnect()
