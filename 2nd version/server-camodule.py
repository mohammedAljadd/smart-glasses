from calendar import c
import io
import socket
import struct
import time
import picamera
from utils import *
import RPi.GPIO as GPIO
from utils import *
from requests.exceptions import Timeout


# GPIO configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

client_socket = socket.socket()

client_socket.connect(('192.168.43.203', 8000))  # ADD IP HERE

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
#play_sound("You are connected to the server, choose your service")

while True:
    if GPIO.input(10) == GPIO.HIGH or GPIO.input(8) == GPIO.HIGH:
        first_button = GPIO.input(8)
        second_button = GPIO.input(10)
        # Choosing the service needed
        # 1: face, 2: object, 3: text
        if first_button:
            service = "01"
            play_sound(service)
        elif second_button:
            service = "10"
            play_sound(service)

        connection.write(bytes(service, encoding='utf8'))

        # Send service

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
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
            connection = open(connection, 'w+')
            connection.write(bytes(service, encoding='utf8'))
            
        finally:
            connection.close()
            client_socket.close()
