import requests
from config import *
from utils import *
import os
import cv2
import pyttsx3  
from requests.exceptions import Timeout
from time import sleep

# Bool variables
is_api = True
too_long = False



# Test internet connection
if not internet_on():
    play_sound("Offline mode is used")
    print("le mode hors ligne est utilisé")
    is_api = False # use offline mode

else:
    play_sound("Online mode is used")
    print("Le mode en ligne est utilisé")


# Wait for push button
while True:
        
        # Taking a picture
        if not take_picture(True):
            pass

        # Choosing the service needed
        # 1: face, 2: object, 3: text
        path = service(1)
        play_sound(path)
        
        

        # Online mode
        if is_api:
            # Sending an http request
            print("Envoi de l'image à l'API")
           
            try:
                image = {'image': open('img/picture.jpg', 'rb')}
                # waiting 5 seconds, if not response, switch to offline mode
                r = requests.post(API_IP_ADD+path, files=image, timeout=10) 
                 
                print("l'image sera traité")
                print(r.text)
                play_sound(r.text)
            except Timeout:
                print("requête http non envoyée")
                is_api = False
                too_long = True
        
        # Offline mode
        if not is_api:
            if too_long:
                print("La connexion Internet est lente, on passe au mode déconnecté")
                play_sound("The Internet connection is slow, we go offline")
            # Text recognition
            if path == "textrecognition":
                img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
                img = cv2.resize(img, (960, 540)) 
                predictions = pytesseract.image_to_string(img)
                result = predictions.replace('\n', ' ')
                if result.isspace() == False:
                #result = str(text_translation(result))
                    result = str(result)
                else:
                    result = "No text is detected"
                # Display result
                print("Here is your result :"+result)
                play_sound(result)


            else:
                model = get_model(path)
                # Facial recognition
                if path == "facialrecognition":
                    result = facial_recognition(model=model, threshold=0.7)
                    print(result)
                    play_sound(result)

                # Object detection
                else:
                    classes = object_detection(image_path, net=model)
                    # Describe the content of the image for the user (blind)
                    describtion  = results(model="yolo", classes=classes)

                    print(describtion)
                    play_sound(describtion)

            
        break
    




