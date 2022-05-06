from gtts import gTTS
import pygame
import cv2
from time import sleep
from v1.config import *

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
        camera.capture('v1/img/picture.jpg')
        camera.stop_preview()
        return True
    except:
        print("La prise de photo a échoué")
        play_sound("Failed to take photo")
        return False
        


# Taking picture function (esp-32 cam)
def take_picture(is_api=True):  
    try:
        print("La prise de photo ...")
        vid = cv2.VideoCapture(CAMERA_IP_ADD)

        while(True):
            ret, frame = vid.read()
            if cv2.imwrite("img/picture.jpg", frame):
                vid.release()
                cv2.destroyAllWindows()
                play_sound("The photo is taken")
                return True
        
    except:
        print("La prise de photo a échoué")
        play_sound("La prise de photo a échoué")
        return False