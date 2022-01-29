import os
from app import app

class DevelopmentConfig(object):
    
    DEBUG = True
    
    ENV = "development"
    
    APP = "run.py"

    SCM_DO_BUILD_DURING_DEPLOYMENT = True

    YOLO_FOLDER = os.path.join(os.path.dirname(__file__), "app/static\\deep_learning_models\\YOLOv4")

    FACE_RECOGNITION_FOLDER = os.path.join(os.path.dirname(__file__), "app\\static\\deep_learning_models\\Face_recognition")
    
    IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "app\\static\\image\\")
  
    AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), "app\\static\\audio\\")

    CASCADE_FOLDER =  os.path.join(os.path.dirname(__file__), "app\\static\\deep_learning_models\\Face_recognition\\cascades\\data")

    IMG_SIZE = 64

    # The 6th category used when probability is lower than the threshold
    CATEGORIES = ["AL Jadd Mohammed", "EL ASRI Nossaiba", "EL NOUBAOUI Nouhaila", "YE Langze", "an unknown person", "I can not recognize this person"]