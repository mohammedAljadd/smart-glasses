import requests
import RPi.GPIO as GPIO
from config import *
from utils import *
import cv2 
from requests.exceptions import Timeout

# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)






# Wait for push button
while True:
    if GPIO.input(10) == GPIO.LOW:
        play_sound("Le bouton a été pressée")
        print("Le bouton a été pressée")
        
        # Taking a picture
        if not take_picture_cam_module():
            break


        # Choosing the service needed
        # 1: face, 2: object, 3: text
        path = service(1)
        
        print("Sending the image to API")

        try:
            image = {'image': open('img/picture.jpg', 'rb')}
            # waiting 5 seconds, if not response, switch to offline mode
            r = requests.post(API_IP_ADD+path, files=image, timeout=10) 
            print("the http request is sent successfully")
            print(r.text)
            play_sound(r.text, is_api=True)
        except Timeout:
            print("La connexion Internet est lente, veuillez réessayer")
            play_sound("La connexion Internet est lente, veuillez réessayer")
            
            
    break
    




