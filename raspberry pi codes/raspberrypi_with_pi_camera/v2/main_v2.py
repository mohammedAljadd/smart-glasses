from http.server import ThreadingHTTPServer
import io
import socket
import struct
import time
import picamera
from utils import *
import RPi.GPIO as GPIO
from utils import *
from requests.exceptions import Timeout
from v2.config import *

    
# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


client_socket = socket.socket()
client_socket2 = socket.socket()
client_socket.settimeout(10.0)
last_time = time.time()
while True:
        
    try:

        # Connecting to the soccet
        client_socket.connect((ip_add, port1))  # ADD IP HERE
        client_socket2.connect((ip_add, port2))
        play_sound("Vous êtes connecté au serveur, choisissez votre service")

        while True:
            if GPIO.input(10) == GPIO.HIGH or GPIO.input(8) == GPIO.HIGH or GPIO.input(12) == GPIO.HIGH or GPIO.input(11) == GPIO.HIGH or GPIO.input(13) == GPIO.HIGH: 
                first_button = GPIO.input(8)
                second_button = GPIO.input(10)
                third_button= GPIO.input(11)
                fourth_button = GPIO.input(12)
                fifth_button = GPIO.input(13)
                # Choosing the service needed
                # 1: face, 2: object, 3: text
                if first_button:
                    service = "Reconnaissance faciale"
                    sent_service = "10"
                    play_sound(service)
                elif second_button:
                    service = "Détection d'objet"
                    sent_service = "01"
                    play_sound(service)

                elif third_button:
                    play_sound("Pas de prédiction de text pour ce mode")
                
                elif fourth_button:
                    play_sound("Fermeture du mode vidéo")
                    break

                elif fifth_button:
                    play_sound("Mauvaise commande")


                first_button = False
                second_button = False
                
                
                if fourth_button != True or third_button != True or fifth_button != True:
                    client_socket.send(bytes(f"{sent_service}", 'utf-8'))
                    # Make a file-like object out of the connection
                    connection = client_socket.makefile('wb')
                    try:
                        camera = picamera.PiCamera()
                        camera.vflip = False
                        camera.resolution = (500, 480)
                        # Start a preview and let the camera warm up for 2 seconds
                        camera.start_preview()
                        time.sleep(2)

                        # Note the start time and construct a stream to hold image data
                        # temporarily (we could write it directly to connection but in this
                        # case we want to find out the size of each capture first to keep
                        # our protocol simple)
                        start = time.time()
                        stream = io.BytesIO()
                        for foo in camera.capture_continuous(stream, 'jpeg'):
                            # Write the length of the capture to the stream and flush to
                            # ensure it actually gets sent
                            connection.write(struct.pack('<L', stream.tell()))
                            connection.flush()
                            # Rewind the stream and send the image data over the wire
                            stream.seek(0)
                            connection.write(stream.read())
                            # If we've been capturing for more than 30 seconds, quit
                            if time.time() - start > 60:
                                break

                            result = client_socket2.recv(256).decode('utf-8')
                            if time.time() > last_time + 2:
                                play_sound(result)
                                last_time = time.time()
                            # Reset the stream for the next capture
                            stream.seek(0)
                            stream.truncate()

                            
                        # Write a length of zero to the stream to signal we're done
                        connection.write(struct.pack('<L', 0))
                    finally:
                        connection.close()
                        client_socket.close()

    except:
        play_sound("Le serveur est inaccessible, veuillez réessayer")