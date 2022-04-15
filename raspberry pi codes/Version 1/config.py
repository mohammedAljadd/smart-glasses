import cv2

# API ip adress
API_ADD = "http://192.168.1.9:5000/"

# Facial recognition classes
CATEGORIES = ["AL Jadd Mohammed", "EL ASRI Nossaiba", "EL NOUBAOUI Nouhaila", "YE Langze", "unknow person", "there is no person"]

# Img size for CNN model
IMG_SIZE = 32

# Image path
#image_path = "img/picture1.jpg"
image_path = "img/testocr.png"

# Face cascade xml file
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# YOLO path
yolo_path = "models/YOLOv4"