from importlib.resources import path
from unicodedata import name
from urllib import response
from flask_restful import  Resource
from app.utils import *
from flask import request
import cv2
import pytesseract
import pathlib

class Facial_Recognition(Resource):
    def post(self):
        return {"msg": "Facial_Recognition"}

class Object_Detection(Resource):
    def post(self):
        return {"msg": "Object_Detection"}

class Text_recognition(Resource):
    def post(self):
        if request.files:
            from app import app
            image = request.files["image"]
            image_path = f"{app.config['IMAGE_FOLDER']}"+"/"+image.filename
            image.save(image_path)
           
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

            img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
            img = cv2.resize(img, (960, 540)) 

            

            predictions = pytesseract.image_to_string(img)
            result = predictions.replace('\n', ' ')
            if len(result)>=1:
                result = str(text_translation(result))
                return {"result": result}
            else:
                return {"result": "No text detected"}
            

    