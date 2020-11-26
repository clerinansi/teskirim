#!/bin/env python

import cv2
import numpy as np
from datetime import datetime
import time
import os
import RPi.GPIO as GPIO
import firebase
from firebase import firebase
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, messaging, db

# Pin Definitons:
relayPin = 23 # Broadcom pin 23 (P1 pin 16)
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(relayPin, GPIO.OUT) # LED pin set as output
# Initial state for LEDs:
GPIO.output(relayPin, GPIO.LOW)

   
cred = credentials.Certificate('/home/pi/cleriproject/Skripsi1/firebasekey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://skripsi-3d93f.firebaseio.com/'
})

path = "/var/www/html/photos"
ext = "jpg"
ts = time.time()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/cleriproject/Skripsi1/trainer/trainer.yml')
cascadePath = '/home/pi/cleriproject/Skripsi1/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

    o
    
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
i = 0

        
def take_photo () :
    global i
    i = i+1
    cvt = str(i)
    st = datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
    file_name = str(Id) + "." + str(st)
    timefile = os.path.join(path, file_name + "."  + cvt + "." + ext)
    s.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/cleriproject/Skripsi1/firebasekey.json"
    firebase = firebase.FirebaseApplication('https://skripsi-3d93f.firebaseio.com/')
    client = storage.Client()
    bucket = client.get_bucket('skripsi-3d93f.appspot.com/') #Dont forget to remove gs:// from the storage database link
    # posting to firebase storage
    imageBlob = bucket.blob("/")
    imageBlob = bucket.blob(filename) #the name you want to save your image as on firebase
    push_notify(file_name + "."  + cvt + "." + ext)
    cv2.imwrite(timefile, im)
    imageBlob.upload_from_filename(path)


def push_notify(filename) :
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    
    registration_tokens = []
    
    dbRef = db.reference("users")
    dataSnapshot = dbRef.order_by_key().get()
    for key, val in dataSnapshot.items():
        registration_tokens.append(key)
        
    #print("token device tersedia : {0}".format(registration_tokens))
   
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification = messaging.Notification(
            title = "Terdeteksi Orang Tidak Dikenal",
            body = filename
        ),
        tokens=registration_tokens,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message, app=default_app)
    if response.failure_count > 0 :
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses): 
            if not resp.success:
                failed_tokens.append(registration_tokens[idx])
        #print("list of failures token: {0}".format(failed_tokens))
    # Response is a message ID string.
    # print('Successfully sent message:', response)


def nyala() :
    dbRef = db.reference("testpin")
    status = dbRef.child("raspi_server_1").child("status")

    if status.get():
        GPIO.output(relayPin, GPIO.HIGH)
        print("NYALA")
        time.sleep(10)
        status.set(False)
        GPIO.output(relayPin, GPIO.LOW)
        print("mati")

        
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])

        print("id{}, confidence{}".format(Id,conf))


        if(conf<50):
             if(Id==1):
                 Id="Cleri Karinda"
             elif(Id==2):
                 Id="Lisa"
             elif(Id==3):
                 Id="David"
             elif(Id==4):
                 Id="mita"
        
        else:
            Id = "Unknown"

            take_photo()
        
        cv2.putText(im, str(Id), (x+5,y-5), font, 1,(255,255,255), 2)
        

    cv2.imshow('terdeteksi',im)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
    nyala()


cam.release()
cv2.destroyAllWindows()


