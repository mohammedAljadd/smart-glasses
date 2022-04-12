from picamera import PiCamera
from time import sleep
import pytesseract
import pyttsx3, time 
from tensorflow.keras.models import load_model

# Service needed
def service(option):
    path = ""
    if option == 1:
        path = "facialrecognition"
    elif option == 2:
        path = "objectrecognition"
    else:
        path = "textrecognition"
    return path

# Taking picture function
def take_picture():
    try:
        camera = PiCamera()
        camera.start_preview()
        sleep(0.5)
        camera.capture('img/picture.jpg')
        camera.stop_preview()
    except:
        print("Camera is not available")

# Generating audio file from a text
def generate_audio(text):
    pass
    #engine = pyttsx3.init() 
    #engine.say(text) 
    #engine.runAndWait()


# Load models
def get_model(service):
    global model
    if service == "facialrecognition":
        model = load_model('models/cnn/cnn_big_model.h5')

    elif service == "objectrecognition":
        model = cv2.dnn.readNet(f"models/yolo/yolov4.weights", f"models/yolo/yolov4.cfg")
    return model

# Faciale recognition
'''
def facial_recognition():

    # Upload folder for images
    imgs_path = "img/"



    # Face cascade xml file
    cascades = ""
    face_cascade = cv2.CascadeClassifier(os.path.join(cascades, 'haarcascade_frontalface_default.xml'))
    
    # Make upload folder empty first
    empty_folder(imgs_path)

    # Save the image
    image = request.files["image"]
    image_name = image.filename
    image_path = imgs_path+image_name
    image.save(image_path)
    
    # Grayscale
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Detected classes indexes
    predictions = []

    # Detect the face with face_cascade
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=8)
    
    if len(faces) != 0:
        
        for (x, y, w, h) in faces:
            face = gray_image[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE)) 
            face_expanded = np.expand_dims(face_resized, axis=0)

            # Normalize the image, the model was trained on normalized images
            face_input = tf.keras.utils.normalize(face_expanded, axis=1)

            # Make prediction
            index = predict(face_input, threshold=0.7)
            predictions.append(index)
        #predictions = list(set(predictions))
        # Count number faces
        predictions = np.array(predictions) #.reshape(predictions.shape[0])
        i = predictions.shape[0]
        
        return result_face_recognition(predictions=predictions, CATEGORIES=CATEGORIES, number_of_faces=i)
        
    return result_face_recognition(CATEGORIES=CATEGORIES)
    *
'''

# tesseract function

def tesseract():
    image_path = "img/picture.jpg"
    
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
    img = cv2.resize(img, (960, 540)) 

    

    predictions = pytesseract.image_to_string(img)
    result = predictions.replace('\n', ' ')
    if len(result)>=1:
        result = str(text_translation(result))
        return {"result": result}
    else:
        return {"result": "No text detected"}