from gtts import gTTS
import os
import pygame




def generate_audio(text):
    language = 'en'
    
    audio = gTTS(
                text=text, 
                lang=language, slow=False
    )

    audio.save("audio/audio.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("audio/audio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
