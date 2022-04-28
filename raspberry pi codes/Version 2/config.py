import cv2

# API ip adress
API_IP_ADD = "http://192.168.43.203:5000/"

# IP@ of ESP-32 cam
CAMERA_IP_ADD = "http://192.168.43.217:81/stream"

# Facial recognition classes
CATEGORIES = ["AL Jadd Mohammed", "EL ASRI Nossaiba", "EL NOUBAOUI Nouhaila", "YE Langze", "unknown person", "there is no person"]

# Img size for CNN model
IMG_SIZE = 32

# Image path
image_path = "img/picture.jpg"
#image_path = "img/testocr.png"

# Face cascade xml file
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# YOLO path
yolo_path = "../models/YOLOv4"

# IP@ of ESP-32 cam
CAMERA_IP_ADD = "http://192.168.43.217:81/stream"