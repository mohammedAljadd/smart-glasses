from flask_restful import  Resource


class Facial_Recognition(Resource):
    def post(self):
        return {"msg": "Facial_Recognition"}

class Object_Detection(Resource):
    def post(self):
        return {"msg": "Object_Detection"}

class Text_recognition(Resource):
    def post(self):
        return {"msg": "Text_recognition"}
            

    