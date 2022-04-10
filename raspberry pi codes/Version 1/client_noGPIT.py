import requests


# API ip adress
BASE = "http://192.168.43.203:5000/"


option = 1
path = ""

if option == 1:
    path = "facialrecognition"
if option == 2:
    path = "objectdetection"
else:
    path = "textrecognition"


image = {'image': open('img/picture.jpg', 'rb')}
r = requests.post(BASE+path, files=image)
print("the http request is sent successfully")
    



