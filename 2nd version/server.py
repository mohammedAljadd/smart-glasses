from msilib.schema import Error
import socket, cv2, pickle,struct,imutils
from utils import *
from config_server import *
import numpy as np
import tensorflow as tf
from time import time
from time import sleep
last_time = time()
font = cv2.FONT_HERSHEY_SIMPLEX
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999

socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

j = 0

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    
    if client_socket:
        print("Client is connected", addr)
        
        # Receive option from client --------------
        option = client_socket.recv(256).decode('utf-8')
        print(option)

        # Ask client for video streaming
        client_socket.send(bytes("Need streaming", 'utf-8'))


        if option == "Object detection":
            model = load_yolo_model()
            print("Yolo model is loaded")
        
        elif option == "Facial recognition":
            model = load_cnn_model()
            face_cascade = cv2.CascadeClassifier(f"{CASCADE_FOLDER}/haarcascade_frontalface_default.xml")
            print("CNN model is loaded")

        elif option == "Text recognition":
            model = load_text_model()
            print("Text model is loaded")
            # Receive image
        
        while True:

            # Receive data 'streaming' -----------------------------------------------------------------------------------
            x = client_socket.recvfrom(1000000)
            clientip = x[1][0]
            data = x[0]
            data = pickle.loads(data)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            

            # Preprocess the image -------------------------------------------------------------------------------------------
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            

            # Prediction Section ---------------------------------------------------------------------------------------------
            if time() > last_time + 0.24:

                if option == "Facial recognition":


                    # Detect the face with face_cascade ----------------------------------------------------------------------
                    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=5)
                    if len(faces) != 0:
                        for (x, y, w, h) in faces:
                            face = gray_image[y:y+h, x:x+w]
                            face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE)) 
                            face_expanded = np.expand_dims(face_resized, axis=0)


                            # Normalize the image, the model was trained on normalized images -------------------------------------
                            face_input = tf.keras.utils.normalize(face_expanded, axis=1)


                            try:
                                # Make prediction -------------------------------------------------------------------------------------
                                index, probabilty = predict(face_input, threshold=0.6, model=model)
                                prediction = CATEGORIES[index]
                            
                            except Exception:
                                prediction = CATEGORIES[6]
                            
                            j += 1


                            # Send back prediction to client ----------------------------------------------------------------------
                            client_socket.send(bytes(f"{prediction} {probabilty}%", 'utf-8'))
                        else:
                            pass
                            #client_socket.send(bytes("No face is detected", 'utf-8'))
                last_time = time()

            cv2.putText(gray_image, "Serveur" , (50,50), font, 1, (255, 0, 0), 6,6)
	
            cv2.imshow('server', gray_image) #to open image
            if cv2.waitKey(10) == 13:
                break
        cv2.destroyAllWindows()
        

        
        

        
        client_socket.close()
        break