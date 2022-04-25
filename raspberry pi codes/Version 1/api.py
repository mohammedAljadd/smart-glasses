from flask import Flask, app
from flask import render_template
app = Flask(__name__)




@app.route("/ip-cam")
def ipcame():
    return render_template("ip-cam.html")



if __name__ == "__main__":
    app.run()