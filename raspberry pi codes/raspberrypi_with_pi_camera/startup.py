import RPi.GPIO as GPIO
from v1.utils import play_sound
import sys
sys.path.append('v1/')
sys.path.append('v2/')
sys.path.append('v1/img/')



# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



play_sound("Choose your mode, image or video")


while True:
    
    if GPIO.input(10) == GPIO.HIGH or GPIO.input(8) == GPIO.HIGH or GPIO.input(12) == GPIO.HIGH or GPIO.input(11) == GPIO.HIGH or GPIO.input(13) == GPIO.HIGH: 
        first_button = GPIO.input(8)
        second_button = GPIO.input(10)
        third_button= GPIO.input(11)
        fourth_button = GPIO.input(12)
        fifth_button = GPIO.input(13)

        # image
        if fourth_button:
            play_sound("Image processing")
            exec(open("v1/main_v1.py").read())
                

        # video    
        elif fifth_button:
            play_sound("Video processing")
            exec(open("v2/main_v2.py").read())
            
        elif first_button or second_button or third_button:
            play_sound("Wrong commande")