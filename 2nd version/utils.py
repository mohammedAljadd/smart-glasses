import numpy as np
from tensorflow.keras.models import load_model
from config_server import *
import cv2
import tensorflow as tf

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



def facial_recognition(model, threshold, face_cascade, gray_image):
    
    # Detected classes indexes
    predictions = []

    # Detect the face with face_cascade
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.7, minNeighbors=5)
    
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
 


def predict(image, threshold, model):
    prediction = model.predict(image)
    index = np.argmax(prediction[0])
    probabilty = float(format(max(prediction[0]*100), ".3f"))

    if probabilty < threshold*100:
        # The 6th category when probability is lower than the threshold
        return 5

    return index, probabilty



import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Load models
def get_model(service):
    global model
    if service == "01":
        model = load_model('static/deep_learning_models/Face_recognition/cnn_big_model.h5')

    elif service == "10":
        model = cv2.dnn.readNet("static/deep_learning_models/YOLOv4/yolov4.weights", "static/deep_learning_models/YOLOv4/yolov4.cfg")
    return model


# Return objects within an image
def object_detection(image, net):
    labels = []
    # Load Yolo
    classes = []
    with open(f"{yolo_path}/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    img = np.array(image)
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


'''
def text_translation(text):
    translator = Translator()
    language = translator.detect(text)
    if language != "fr":
        translated_text = translator.translate(text, dest='fr')
        return translated_text.text
    return text
'''
    

# Return result as a human understood text
def results(classes):
    from collections import Counter
    list_objects_counted = []
    final_result = "Il y'a  "
    nb_classes = len(classes)
    if nb_classes == 0:
        return f"Rien n'est détecté"
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

                          