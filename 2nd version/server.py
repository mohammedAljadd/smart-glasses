import io
import socket
import struct
from PIL import Image
from grpc import server
import matplotlib.pyplot as pl
from threading import Thread
from utils import *
from time import time
from config_server import *

last_time = time()
server_socket = socket.socket()
server_socket2 = socket.socket()
server_socket.bind((ip_add, port1))  # ADD IP HERE
server_socket2.bind((ip_add, port2)) 
server_socket.listen(0)
server_socket2.listen(0)
client_socket,addr = server_socket2.accept()
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

# Receive option from raspberry pi
service = connection.readline(2).decode("UTF-8")




try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

       
        pl.pause(0.01)
        pl.draw()

        image.verify()
        
        # Prediction
        img_array = np.asarray(image)
        gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        model = get_model(service)
        if service == "01":
            import os
            face_cascade = cv2.CascadeClassifier(os.path.join(CASCADE_FOLDER, 'haarcascade_frontalface_default.xml'))
            result = facial_recognition(model, threshold=0.7, face_cascade=face_cascade, gray_image=gray_image)
            client_socket.send(bytes(result, 'utf-8'))
            
                
        elif service == "10":
            labels = object_detection(image, model)
            result = results(labels)
            client_socket.send(bytes(result, 'utf-8'))
            
        
        


finally:
    connection.close()
    server_socket.close()