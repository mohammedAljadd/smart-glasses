from gtts import gTTS
import pygame
import cv2
from time import sleep
from v1.config import *
import numpy as np

# Text to audio
def play_sound(text):
    
    audio = gTTS(
            text=text, 
            lang="fr", slow=False
            )
    audio_file_path = "audio/audio.mp3"
    audio.save(audio_file_path)
    
    pygame.mixer.init()
    pygame.mixer.music.load("audio/audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
        




# Service needed
def service(option):
    path = ""
    if option == 1:
        path = "facialrecognition"
    elif option == 2:
        path = "objectdetection"
    else:
        path = "textrecognition"
    return path

# Taking picture function (raspberry pi cam module)
def take_picture_cam_module(camera): 
    try:
        camera.start_preview()
        sleep(0.5)
        camera.capture(image_path)
        camera.stop_preview()
        play_sound("La photo a été prise")
        return True
    except:
        print("La prise de photo a échoué")
        play_sound("La prise de photo a échoué")
        return False
        


# Taking picture function (esp-32 cam)
def take_picture(is_api=True):  
    try:
        print("La prise de photo ...")
        vid = cv2.VideoCapture(CAMERA_IP_ADD)

        while(True):
            ret, frame = vid.read()
            if cv2.imwrite(image_path, frame):
                vid.release()
                cv2.destroyAllWindows()
                play_sound("La photo a été prise")
                return True
        
    except:
        print("La prise de photo a échoué")
        play_sound("La prise de photo a échoué")
        return False


# Return objects within an image
def object_detection(image):
    labels = []
    # Load Yolo
    yolo_path = "/home/pi/Desktop/rasp-elec/deep_learning_models/YOLOv4"
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

# Return result as a human understood text
def results(model, classes):
    from collections import Counter
    list_objects_counted = []
    final_result = "Il y'a  "
    if model == "yolo":
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

                          

    elif model == "face":
        pass
    elif model == "text":
        pass
    else:
        pass
