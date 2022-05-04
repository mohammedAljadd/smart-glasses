from email.mime import image
import imp
from pyexpat import model
from sre_parse import CATEGORIES
from statistics import mode
import numpy as np
import cv2
from gtts import gTTS
from mutagen.wave import WAVE
from googletrans import Translator
import os
from tensorflow.keras.models import load_model



def generate_audio(string):
    from app import app
    audio = gTTS(
                text=string, 
                lang="en", slow=False
                )

    audio_file_path = app.config["AUDIO_FOLDER"]+"audio.mp3"
    audio.save(audio_file_path)
    return "audio.mp3"
    

def get_model():
    from app import app
    global model
    model = load_model(os.path.join(app.config['FACE_RECOGNITION_FOLDER'],'cnn_big_model.h5'))
    return model


    
def predict(image, threshold):
    from app import app
    model = get_model()
    prediction = model.predict(image)
    index = np.argmax(prediction[0])
    probabilty = float(format(max(prediction[0]*100), ".3f"))

    if probabilty < threshold*100:
        # The 4th category when probability is lower than the threshold
        return 4

    return index



# Return objects within an image
def object_detection(image):
    from app import app
    labels = []
    # Load Yolo
    yolo_path = f"{app.config['YOLO_FOLDER']}"
    net = cv2.dnn.readNet(f"{yolo_path}/yolov4.weights", f"{yolo_path}/yolov4.cfg")
    classes = []
    with open(f"{yolo_path}/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    img = cv2.imread(image)
    img = cv2.resize(img, None, fx=0.9, fy=0.9)
    height, width, channels = img.shape


    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)


    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            labels.append(label)
            
    return labels



def text_translation(text):
    translator = Translator()
    language = translator.detect(text)
    if language != "fr":
        translated_text = translator.translate(text, dest='fr')
        return translated_text.text
    return text

    

# Return result as a human understood text
def results(model, classes):
    from collections import Counter
    list_objects_counted = []
    final_result = "Il y'a  "
    if model == "yolo":
        nb_classes = len(classes)
        if nb_classes == 0:
            return f"Rien n'est d\xe9tect\xe9"
        elif nb_classes == 1:
            return f"Il y'a {classes[0]}"
        else:
            result = Counter(classes)
            new_listed = []
            for e in result:
                if result[e] > 1:
                    x = e.split(' ')
                    string = ' '.join([n for n in x[1:]])
                    new_listed.append(str(result[e])+' '+string+'s')
            else:
                # Let 'un' or 'une' if the number of occurences is equal to 1.
                new_listed.append(e)

            # new_listed contains elements with their number of occurences. Eg: 3 bottles, 2 chairs.
            
            '''
            first = True
            for r in result:
                if result[r] > 1:
                    if first:
                        list_objects_counted.append(str(result[r])+" "+r+"s")
                        first = False
                    else:
                        list_objects_counted.append(str(result[r])+" "+r+"s")
                else:
                    if first:
                        list_objects_counted.append(str(result[r])+" "+r)
                        first = False
                    else:
                        list_objects_counted.append(str(result[r])+" "+r)
                
            n = len(list_objects_counted)
            i = 0
            for element in list_objects_counted:
                if i < n-2:
                    final_result += element+", "
                elif i == n-2:
                    final_result += element+" et "
                else:
                    final_result += element+"."
                i += 1
            '''
            n = len(new_listed)
            i = 0
            for element in new_listed:
                if i < n-2:
                    final_result += element+", "
                elif i == n-2:
                    final_result += element+" et "
                else:
                    final_result += element+"."
                i += 1
            return final_result

                          

    elif model == "face":
        pass
    elif model == "text":
        pass
    else:
        pass


def audio_lenght(text):
    pass
    
def empty_folder(path):
    for img in os.listdir(path):
        filename = os.path.join(path,img)
        os.remove(filename)


def result_face_recognition(predictions=[5], CATEGORIES=CATEGORIES, number_of_faces=0):

    if number_of_faces == 0 and predictions[0] == 5:
        result = "Il n'y a personne."

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

        result = "Il y'a "
        if number_of_faces == 1:
            result += f"{replace(occurences[0])} {CATEGORIES[predictions[0]]}"

        elif number_of_faces == 2:
            result += f" {replace(occurences[0])} {CATEGORIES[predictions[0]]} et {replace(occurences[1])} {CATEGORIES[predictions[1]]}"

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


# Functions for Handwritting recognition

def getHProjection(image):

    hProjection = np.zeros(image.shape,np.uint8)

    #height and width of image

    (h,w)=image.shape

    #length of array same as height of image
 
    h_ = [0]*h

    #count up the number of white pixels in every line

    for y in range(h):

        for x in range(w):

            if image[y,x] == 255:

                h_[y]+=1

    #draw the horizontal projection 

    for y in range(h):

        for x in range(h_[y]):

            hProjection[y,x] = 255

    ##################################################cv2.imshow('hProjection2',hProjection)

 

    return h_

 

def getVProjection(image):

    vProjection = np.zeros(image.shape,np.uint8);

    #heigth and width of image

    (h,w) = image.shape

    #length of array same as width of image

    w_ = [0]*w

    #count up the number of white pixels in every column

    for x in range(w):

        for y in range(h):

            if image[y,x] == 255:

                w_[x]+=1

    #draw the projection vertical

    for x in range(w):

        for y in range(h-w_[x],h):

            vProjection[y,x] = 255

    #cv2.imshow('vProjection',vProjection)

    return w_

 