#-*- coding:utf-8 -*-

import cv2
import tensorflow as tf
import numpy as np   
from keras.preprocessing.image import img_to_array
from keras.models import load_model



face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotion_classifier = load_model('emotion1.hdf5', compile=False)
EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']


camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    # Capture image from camera
    ret, frame = camera.read()
    
    # Convert color to gray scale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # Face detection in frame
    faces = face_detection.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30,30))
    
       
    # display only face detected
    if len(faces) > 0:
        face = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = face
        # Resize the image to 64*64 for neural network
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        
        # Emotion predict
        preds = emotion_classifier.predict(roi)[0]        
        score = tf.nn.softmax(preds)   
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        
        # draw face detect frame
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (255, 255, 255), 1)
 
        # display emotion predict
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            text = "%-10s" % f"{emotion}"    
            w = int(prob * 300)
            cv2.rectangle(frame, (100, (i * 20) + 12), (round(w*0.5) + 100, (i * 20) + 22), (102, 204, 102), -1)
            cv2.putText(frame, text, (7, (i * 20) + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

   #display frame
    cv2.imshow('emotion', frame)
    
    # esc to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()