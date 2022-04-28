import requests
import RPi.GPIO as GPIO
from utilsrasp import generate_audio
from config import *
from utilsrasp import *
import os
import cv2
import pyttsx3  

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Bool variables
is_api = True
too_long = False


# Test internet connection
if not internet_on():
    play_sound("The server is currently unreachable, offline mode is activated", is_api)
    print("The server is currently unreachable, offline mode is activated")
    is_api = False # use offline mode

else:
    play_sound("Online mode is used", is_api)
    print("Online mode is used")


# Wait for push button
while True:
    if GPIO.input(10) == GPIO.LOW:
        play_sound("The button is pushed successfully", is_api)
        print("The button is pushed successfully")
        
        # Choosing the service needed
        # 1: face, 2: object, 3: text
        path = service(2)
        
        # Taking a picture
        take_picture()
        print("The picture is taken successfully")
        play_sound("The picture is taken successfully", is_api)
        

        # Online mode
        if is_api:
            # Sending an http request
            print("Sending the image to API")

            try:
                image = {'image': open('img/picture.jpg', 'rb')}
                # waiting 5 seconds, if not response, switch to offline mode
                r = requests.post(API_IP_ADD+path, files=image, timeout=8) 
                print("the http request is sent successfully")
                print(r.text)
                play_sound(r.text, is_api)
            except:
                print("http not sent")
                is_api = False
                too_long = True
        
        # Offline mode
        if not is_api:
            if too_long:
                print("La requête http met trop de temps à répondre, on passe en mode déconnecté")
                play_sound("La requête http met trop de temps à répondre, on passe en mode déconnecté", is_api)
            # Text recognition
            if path == "textrecognition":
                img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
                img = cv2.resize(img, (960, 540)) 
                predictions = pytesseract.image_to_string(img)
                result = predictions.replace('\n', ' ')
                if len(result)>=1:
                    result = str(result)
                else:
                    result = "No text detected"
                # Display result
                print("Here is your result :"+result)
                play_sound(result, is_api)


            else:
                model = get_model(path)
                # Facial recognition
                if path == "facialrecognition":
                    result = facial_recognition(model=model, threshold=0.7)
                    print(result)
                    play_sound(result, is_api)

                # Object detection
                else:
                    classes = object_detection(image_path, net=model)
                    # Describe the content of the image for the user (blind)
                    describtion  = results(model="yolo", classes=classes)

                    # Create an audio file from the previous text
                    audio = generate_audio(describtion)
                    #return send_from_directory(directory=app.config['AUDIO_FOLDER'], path="audio.mp3", as_attachment=True)
                    response = {
                        "result": describtion
                    }
                    print(describtion)
                    play_sound(describtion, is_api)

            
    break
    




