from gtts import gTTS
import pygame

from time import sleep

# Text to audio
def play_sound(text):
    
    audio = gTTS(
            text=text, 
            lang="en", slow=False
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
        


