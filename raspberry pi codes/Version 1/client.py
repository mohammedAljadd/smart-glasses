import requests
import RPi.GPIO as GPIO
from audio import generate_audio


# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# API ip adress
BASE = "http://192.168.43.203:5000/"


option = 1
path = ""


# Wait for push button
while True:
    if GPIO.input(10) == GPIO.LOW:
        #generate_audio("The button is pushed successfully")
        print("The button is pushed successfully")
        
        
        # Take a picture
        exec(open("picture.py").read())
        print("The picture is taken successfully")
        
        
        # Choose service
        if option == 1:
            path = "facialrecognition"
        elif option == 2:
            path = "objectrecognition"
        else:
            path = "textrecognition"
        
        
        # Send http request
        image = {'image': open('img/picture.jpg', 'rb')}
        r = requests.post(BASE+path, files=image)
        print("the http request is sent successfully")
        
        print(r.text)
        
    break
    



