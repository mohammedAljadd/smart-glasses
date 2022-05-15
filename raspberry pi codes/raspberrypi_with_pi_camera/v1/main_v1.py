from numpy import unicode_
import requests
import RPi.GPIO as GPIO
from config import *
from utils import *
import cv2 
from requests.exceptions import Timeout
from picamera import PiCamera


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
            print("Détection d'objet")
            play_sound("Détection d'objet")

        elif third_button:
            path = service(3)
            print("Reconnaissance de texte")
            play_sound("Reconnaissance de texte")
        
        elif fourth_button:
            play_sound("Mauvaise commande")
    
            
            
        elif fifth_button:
            play_sound("Fermeture du mode image")
            camera.close()
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
                image = {'image': open('v1/img/picture.jpg', 'rb')}
                # waiting 5 seconds, if not response, switch to offline mode
                print("Sending to API")
                r = requests.post(API_IP_ADD+path, files=image, timeout=10) 
                result = r.json()
                # Decode french characters
                result = result.replace('Ã©', 'é')
                
                result = result.replace('Ãª', 'ê')
                
                result = result.replace('Ã¨', 'è')
                
                result = result.replace('Ã', 'à')
                print(result)
                
                play_sound(result)
            except Timeout:
                print("La connexion Internet est lente, On passe au mode hors ligne")
                camera.close()
                exec(open("v1/main_v1_offline.py").read())
            
        else:
            fourth_button = False
            
    