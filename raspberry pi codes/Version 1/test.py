import requests
image = {'image': open('img/picture.jpg', 'rb')}
r = requests.post("http://192.168.43.244:5000/objectdetection", files=image) 