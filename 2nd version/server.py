import socket, cv2, pickle,struct,imutils
from utils import *


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
            model = load_lbph_model()
            print("LBPH model is loaded")

        elif option == "Text recognitio":
            model = load_text_model()
            print("Text model is loaded")
        
        for i in range(10):
             streaming = client_socket.recv(256).decode('utf-8')
             print(f"{streaming}\n")
        

        
        

        
        client_socket.close()
        break