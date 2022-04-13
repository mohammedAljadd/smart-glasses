#from picamera import PiCamera
from time import sleep
import pytesseract
import pyttsx3, time 
#from tensorflow.keras.models import load_model
from tensorflow import keras
from config import *
import cv2
import tensorflow as tf
import numpy as np

# Service needed
def service(option):
    path = ""
    if option == 1:
        path = "facialrecognition"
    elif option == 2:
        path = "objectrecognition"
    else:
        path = "textrecognition"
    return path

# Taking picture function
def take_picture():
    try:
        camera = PiCamera()
        camera.start_preview()
        sleep(0.5)
        camera.capture('img/picture.jpg')
        camera.stop_preview()
        print("The picture is taken successfully")
    except:
        print("The camera is not available")

# Generating audio file from a text
def generate_audio(text):
    pass
    #engine = pyttsx3.init() 
    #engine.say(text) 
    #engine.runAndWait()


# Load models
def get_model(service):
    global model
    if service == "facialrecognition":
        model = keras.models.load_model('../models/Face_recognition/cnn_big_model.h5')

    elif service == "objectrecognition":
        model = cv2.dnn.readNet(f"models/yolo/yolov4.weights", f"models/yolo/yolov4.cfg")
    return model

# Faciale recognition

def facial_recognition(model, threshold, face_cascade=face_cascade):
    
    

    # Grayscale
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Detected classes indexes
    predictions = []

    # Detect the face with face_cascade
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=2, minNeighbors=5)
    
    if len(faces) != 0:
        
        for (x, y, w, h) in faces:
            face = gray_image[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE)) 
            face_expanded = np.expand_dims(face_resized, axis=0)

            # Normalize the image, the model was trained on normalized images
            face_input = tf.keras.utils.normalize(face_expanded, axis=1)

            # Make prediction
            prediction = model.predict(face_input)
            index = np.argmax(prediction[0])
            probabilty = float(format(max(prediction[0]*100), ".3f"))

            if probabilty < threshold*100:
                # The 4th category when probability is lower than the threshold
                index = 4

            predictions.append(index)
        #predictions = list(set(predictions))
        # Count number faces
        predictions = np.array(predictions) #.reshape(predictions.shape[0])
        i = predictions.shape[0]
        
        return result_face_recognition(predictions=predictions, CATEGORIES=CATEGORIES, number_of_faces=i)
        
    return result_face_recognition(CATEGORIES=CATEGORIES)
    

# tesseract function

def tesseract():
    image_path = "img/picture.jpg"
    
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




def result_face_recognition(predictions=[5], CATEGORIES=CATEGORIES, number_of_faces=0):

    if number_of_faces == 0 and predictions[0] == 5:
        result = "il n'y a personne."

    else:

        # Remove duplicates
        predictions_no_duplicates = []
        for i in predictions:
            if i not in predictions_no_duplicates:
                predictions_no_duplicates.append(i)

        number_of_faces = len(predictions_no_duplicates)

        # Count occurences
        occurences = []
        for p in predictions_no_duplicates:
            occurence = predictions.tolist().count(p)
            # Do not consider duplicates of faces of known people, because it's due to face cascade errors
            if p not in [0, 1, 2, 3]:
                occurences.append(occurence)
            else:
                occurences.append(1)


        # Remove index of "no person is detected"
        if number_of_faces >=2 and 5 in predictions_no_duplicates:
            index_no_person = predictions_no_duplicates.index(5)
            predictions_no_duplicates.pop(index_no_person)
            occurences.pop(index_no_person)
            number_of_faces -= 1    

        def replace(i):
            if i == 1:
                return ""
            else:
                return str(i)

        result = "Il y a "
        if number_of_faces == 1:
            result += f"{replace(occurences[0])} {CATEGORIES[predictions[0]]}"

        elif number_of_faces == 2:
            result += f"{replace(occurences[0])} {CATEGORIES[predictions[0]]} et {replace(occurences[1])} {CATEGORIES[predictions[1]]}"

        else:
            
            i = 0
            for p in predictions_no_duplicates:
                if i < number_of_faces:
                    if number_of_faces == 1:
                        result += f"{replace(occurences[i])} {CATEGORIES[p]}."
                    else:
                        result += f"{replace(occurences[i])} {CATEGORIES[p]}, "
                else:
                    result += f"et {replace(occurences[i])} {CATEGORIES[p]}."
                i += 1
    return result