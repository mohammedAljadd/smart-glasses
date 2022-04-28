import socket,cv2, pickle
from utils import *

# create socket
client_socket = socket.socket()#socket.AF_INET,socket.SOCK_STREAM)
#client_socket.settimeout(5)
host_ip = "192.168.43.203"#socket.gethostbyname(host_name)
port = 14390

# Connect to the server --------------------------------------------------------------------------------
try:
    
    print("Trying to connect to "+host_ip+":"+str(port))
    client_socket.connect((host_ip, port)) # a tuple
    
    print("Le serveur est accessible")
    play_sound("Le serveur est accessible")


    # Get option --------------------------------------------------------------------------------
    option = "1"

    if option == "1":
        option = "Facial recognition"

    elif option == "2":
        option = "Object detection"
    else:
        option = "Text recognition"

        

    # Send option ------------------------------------------------------------------------------------------
    client_socket.send(bytes(f"{option}", 'utf-8'))

    import sys
    while True:
        data = client_socket.recv(1024*2).decode('utf-8')
        if not data: sys.exit(0)
        print(data)

except socket.error:
    
    # ----------- video locally

    print("Traitement vidéo local")
    play_sound("Traitement vidéo local")




        
    




client_socket.close()