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



play_sound("Which service you need")

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
            play_sound("Facial recognition")

        elif second_button:
            path = service(2)
            play_sound("Object detection")

        elif third_button:
            path = service(3)
            play_sound("Text recognition")
            
        elif fifth_button:
            play_sound("Closing image processing")
            break


        
        # Taking a picture
        take_picture_cam_module(camera)
        


        
        

        first_button = False
        second_button = False
        print("Sending the image to API")

        try:
            image = {'image': open('v1/img/picture.jpg', 'rb')}
            # waiting 5 seconds, if not response, switch to offline mode
            r = requests.post(API_IP_ADD+path, files=image, timeout=10) 
            print("the http request is sent successfully")
            print(r.text)
            play_sound(r.text)
        except Timeout:
            print("La connexion Internet est lente, veuillez réessayer")
            play_sound("Internet connection is slow, please try again")
            
        
            
    