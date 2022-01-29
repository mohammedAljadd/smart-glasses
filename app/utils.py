from email.mime import image
import imp
from pyexpat import model
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
    model = get_model()
    prediction = model.predict(image)
    index = np.argmax(prediction[0])
    probabilty = float(format(max(prediction[0]*100), ".3f"))
    result = ""
    CATEGORIES = ["aljadd", "nossaiba", "nouhaila", "langze", "unknown"]
    if probabilty < threshold*100:
        result = "I can not recognize this person"
    else:
        title = f"It's {probabilty}% {CATEGORIES[index]} "
 
    return title



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
    final_result = "There "
    if model == "yolo":
        nb_classes = len(classes)
        if nb_classes == 0:
            return "Nothing is detected"
        elif nb_classes == 1:
            return f"There is a {classes[0]} in front of you"
        else:
            result = Counter(classes)
            first = True
            for r in result:
                if result[r] > 1:
                    if first:
                        list_objects_counted.append("are "+str(result[r])+" "+r+"s")
                        first = False
                    else:
                        list_objects_counted.append(str(result[r])+" "+r+"s")
                else:
                    if first:
                        list_objects_counted.append("is "+str(result[r])+" "+r)
                        first = False
                    else:
                        list_objects_counted.append(str(result[r])+" "+r)
                
            n = len(list_objects_counted)
            i = 0
            for element in list_objects_counted:
                if i < n-2:
                    final_result += element+", "
                elif i == n-2:
                    final_result += element+" and "
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