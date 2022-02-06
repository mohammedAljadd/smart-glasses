from importlib.resources import path
from unicodedata import name
from urllib import response
from flask_restful import  Resource
from app.utils import *
from flask import request
import cv2
import pytesseract
import pathlib
import tensorflow as tf

class Facial_Recognition(Resource):
    def post(self):
        if request.files:
            
            from app import app

            # Upload folder for images
            imgs_path = app.config['IMAGE_FOLDER']

            # Image size that the model was trained on
            IMG_SIZE = app.config['IMG_SIZE'] 

            CATEGORIES = app.config["CATEGORIES"]

            # Face cascade xml file
            cascades = app.config['CASCADE_FOLDER']
            face_cascade = cv2.CascadeClassifier(os.path.join(cascades, 'haarcascade_frontalface_default.xml'))
            
            # Make upload folder empty first
            empty_folder(imgs_path)

            # Save the image
            image = request.files["image"]
            image_name = image.filename
            image_path = imgs_path+image_name
            image.save(image_path)
            
            # Grayscale
            gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Detected classes indexes
            predictions = []

            # Detect the face with face_cascade
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.5, minNeighbors=8)
            
            if len(faces) != 0:
                
                
                for (x, y, w, h) in faces:
                    face = gray_image[y:y+h, x:x+w]
                    face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE)) 
                    face_expanded = np.expand_dims(face_resized, axis=0)

                    # Normalize the image, the model was trained on normalized images
                    face_input = tf.keras.utils.normalize(face_expanded, axis=1)

                    # Make prediction
                    index = predict(face_input, threshold=0.7)
                    predictions.append(index)
                #predictions = list(set(predictions))
                # Count number faces
                predictions = np.array(predictions) #.reshape(predictions.shape[0])
                i = predictions.shape[0]
                

                return result_face_recognition(predictions=predictions, CATEGORIES=CATEGORIES, number_of_faces=i)
     
            return result_face_recognition(CATEGORIES=CATEGORIES)
            
            #predictions = predictions#.tolist()
            
# Code pour faire Prédiction visage (le code est caché puisqu'il est long)

class Object_Detection(Resource):
    def post(self):
        if request.files:
            from app import app
            empty_folder(app.config['IMAGE_FOLDER'])
            image = request.files["image"] 
            image_path = f"{app.config['IMAGE_FOLDER']}"+"/"+image.filename
            image.save(image_path)

            # Yolo object detection
            classes = object_detection(image_path)

            # Describe the content of the image for the user (blind)
            describtion  = results(model="yolo", classes=classes)

            # Create an audio file from the previous text
            audio = generate_audio(describtion)
            #return send_from_directory(directory=app.config['AUDIO_FOLDER'], path="audio.mp3", as_attachment=True)
            response = {
                "result": describtion
            }
            return describtion
# Code pour faire Prédiction d'objets (le code est caché)

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
# Code pour faire Prédiction de texte (le code est caché)

    