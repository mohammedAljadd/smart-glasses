import numpy as np
from tensorflow.keras.models import load_model
from config_server import *

def load_yolo_model():
    pass

def load_text_model():
    pass

def load_lbph_model():
    pass

def load_cnn_model():
    model = load_model(FACE_RECOGNITION_FOLDER)
    return model


def predict(image, threshold, model):
    prediction = model.predict(image)
    index = np.argmax(prediction[0])
    probabilty = float(format(max(prediction[0]*100), ".3f"))

    if probabilty < threshold*100:
        # The 6th category when probability is lower than the threshold
        return 5

    return index, probabilty



import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP