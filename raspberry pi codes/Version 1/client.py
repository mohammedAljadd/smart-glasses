import requests
import RPi.GPIO as GPIO
#from audio import generate_audio


# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# API ip adress
BASE = "http://192.168.43.232:5000/"


option = 1
path = ""


# Wait for push button
while True:
    if GPIO.input(10) == GPIO.LOW:
        generate_audio("Button pushed")
        print("Button pushed")
        
        
        # Take a picture
        exec(open("picture.py").read())
        print("Picture taken")
        
        
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
        print("http request sent")
        
        print(r.text)
    break



