from numpy import unicode_
import requests
import RPi.GPIO as GPIO
from config import *
from utils import *
import cv2 
from requests.exceptions import Timeout
from picamera import PiCamera
import pytesseract

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


camera = PiCamera()


print("De quel service avez-vous besoin?")
play_sound("De quel service avez-vous besoin?")

# Wait for push button
while True:
   
    if GPIO.input(10) == GPIO.HIGH or GPIO.input(8) == GPIO.HIGH or GPIO.input(12) == GPIO.HIGH or GPIO.input(11) == GPIO.HIGH or GPIO.input(13) == GPIO.HIGH: 
        first_button = GPIO.input(8)
        second_button = GPIO.input(10)
        third_button= GPIO.input(11)
        fourth_button = GPIO.input(12)
        fifth_button = GPIO.input(13)
        

        # Choosing the service needed
        # 1: face, 2: object, 3: text
        if first_button:
            path = service(1)
            print("Reconnaissance faciale")
            play_sound("Reconnaissance faciale")

        elif second_button:
            path = service(2)
            print("Détection d'objets")
            play_sound("Détection d'objet")

        elif third_button:
            path = service(3)
            print("Reconnaissance de texte")
            play_sound("Reconnaissance de texte")
        
        elif fourth_button:
            play_sound("Mauvaise commande")
    
            
            
        elif fifth_button:
            camera.close()
            play_sound("Fermeture du mode image")
            break


        
        # Taking a picture
        take_picture_cam_module(camera)
        
        #take_picture(is_api=True)


        
        

        first_button = False
        second_button = False
        third_button= False
        fifth_button = False
        
        
        if fourth_button != True:

            try:
                if path == "objectdetection":
                    classes = object_detection(image=image_path)
                    # Describe the content of the image for the user (blind)
                    describtion  = results(model="yolo", classes=classes)
                    print(describtion)
                    play_sound(describtion)
                
                elif path == "textrecognition":
                    img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
                    img = cv2.resize(img, (960, 540)) 
                    predictions = pytesseract.image_to_string(img)
                    result = predictions.replace('\n', ' ')
                    if result.isspace() == False:
                    #result = str(text_translation(result))
                        result = str(result)
                    else:
                        result = "Aucun texte n'est détecté"
                    # Display result
                    print(result)
                    play_sound(result)

                else:
                    pass
            except Timeout:
                print("Le modele ne marche pas")
                play_sound("Le modele ne marche pas")
                
                
            
        else:
            fourth_button = False
            
    