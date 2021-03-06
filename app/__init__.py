# Import needed packages
from flask import Flask, app
from flask_restful import Api
from app.resources import *

# App instanciation
app = Flask(__name__)


@app.route("/test")
def hello():
    return "Flask is working"

# App configuration
app.config.from_object("config.DevelopmentConfig")

# RestAPI
api = Api(app)


# Adding resources to RestAPI
api.add_resource(Facial_Recognition, "/facialrecognition")
api.add_resource(Object_Detection, "/objectdetection")
api.add_resource(Text_recognition, "/textrecognition")
api.add_resource(Text_recognition_HTR, "/textrecognitionHTR")

