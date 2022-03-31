import socket,cv2, pickle,struct
from time import sleep
import sys
from threading import Thread

# create socket, TCP protocol
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999

# Connect to the server --------------------------------------------------------------------------------
client_socket.connect((host_ip, port)) # a tuple






# Get option

option = "1"#input("What service you want?\n1-Facial recognition.\n2-Object detection.\n3-Text recognition.\n")

if option == "1":
	option = "Facial recognition"

elif option == "2":
	option = "Object detection"
else:
	option = "Text recognition"

	

# Send option ------------------------------------------------------------------------------------------
client_socket.send(bytes(f"{option}", 'utf-8'))





# Receive message where asked to stream
asked_streaming = client_socket.recv(256).decode('utf-8')


# Text with no streaming
if option == "Text recognition":
	# Send image
	pass



# Start streaming --------------------------------------------------------------------------------------
cap = cv2.VideoCapture(0)
IMG_SIZE = 288
Started_prediction = False
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
		
	ret,photo = cap.read()
	cv2.putText(photo, "Client" , (50,50), font, 1, (255, 0, 0), 2,2)
	cv2.imshow('Client camera', photo)
	#photo = cv2.resize(photo, (IMG_SIZE, IMG_SIZE))
	ret, buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	x_as_bytes = pickle.dumps(buffer)
	client_socket.sendto((x_as_bytes),(host_ip, port))
	
	# Receive message from server 'Thread'
	def receive_from_server():
		import sys
		while True:
			data = client_socket.recv(1024).decode('utf-8')
			if not data: sys.exit(0)
			print(data)
	Thread(target=receive_from_server).start()


	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break

	


cv2.destroyAllWindows()
cap.release()


client_socket.close()

