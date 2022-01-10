import os
from app import app

class DevelopmentConfig(object):
    
    DEBUG = True
    
    ENV = "development"
    
    APP = "run.py"

    MODEL_FOLDER = os.path.join(app.root_path)+"/static/deep_learning_models/"
    
    IMAGE_FOLDER = os.path.join(app.root_path)+"/static/image/"
    
    AUDIO_FOLDER = os.path.join(app.root_path)+"/static/audio/"