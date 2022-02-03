import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999


# Connect to the server --------------------------------------------------------------------------------
client_socket.connect((host_ip,port)) # a tuple


# Send option ------------------------------------------------------------------------------------------
client_socket.send(bytes("Object detection", 'utf-8'))

# Receive message where asked to stream
asked_streaming = client_socket.recv(256).decode('utf-8')

# Start streaming --------------------------------------------------------------------------------------
for i in range(10):
    client_socket.send(bytes("Streaming", 'utf-8'))


client_socket.close()