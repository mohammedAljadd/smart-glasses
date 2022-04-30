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
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


camera = PiCamera()

first_button = False
second_button = False

# Wait for push button
while True:
    if GPIO.input(10) == GPIO.HIGH or GPIO.input(8) == GPIO.HIGH:
        first_button = GPIO.input(8)
        second_button = GPIO.input(10)
        # Choosing the service needed
        # 1: face, 2: object, 3: text
        if first_button:
            path = service(1)
            play_sound(path)
        elif second_button:
            path = service(2)
            play_sound(path)


        #play_sound("The button is pushed successfully")
        #print("The button is pushed successfully")
        
        # Taking a picture
        if not take_picture_cam_module(camera):
            pass


        
        

        first_button = False
        second_button = False
        print("Sending the image to API")

        try:
            image = {'image': open('img/picture.jpg', 'rb')}
            # waiting 5 seconds, if not response, switch to offline mode
            r = requests.post(API_IP_ADD+path, files=image, timeout=10) 
            print("the http request is sent successfully")
            print(r.text)
            play_sound(r.text)
        except Timeout:
            print("La connexion Internet est lente, veuillez réessayer")
            play_sound("Internet connection is slow, please try again")
            
        
            
    
    