# Text to audio
def play_sound(text, is_api=True):
    if is_api == True:
        from gtts import gTTS
        audio = gTTS(
                text=text, 
                lang="en", slow=False
                )
        audio_file_path = "audio/audio.mp3"
        audio.save(audio_file_path)
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("audio/audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        