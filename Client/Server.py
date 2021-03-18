from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
import threading
import argparse
import datetime
import imutils
import time
import cv2
from copy import deepcopy
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO
from VisionAlgorithms.YOLO.TinyYOLO import TinyYOLO
from VisionAlgorithms.BackgroundSubtraction import BackgroundSubtraction
from EmailReporter import EmailReporter
from TwitterReporter import TwitterReporter
import base64
import math
# from DiscordReporter import DiscordReporter

# python Server.py --ip 192.168.0.27 --port 8000
# python Server.py --ip 127.0.0.1 --port 8000
# python3 Server.py --ip 192.168.56.1 --port 8000
# python3 Server.py --ip 127.0.0.1 --port 8000
# http://camera.butovo.com/mjpg/video.mjpg

# Initialise output frame and a lock to allow
# thread safe exchange of output frames
outputFrame = None
lock = threading.Lock()

# # Https
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

# Initialize a flask object
app = Flask(__name__)

# Initialize boxes
box = (0, 0, 0, 0)

# Minimum size for contours
minSize = 900

# Create video stream
vs = VideoStream(src=0).start()
time.sleep(1)

t = None

md = Motion()

reporter = None

# Algo settings
minSize = 0
maxSize = 100
boxType = None

count = 0
frameCount = 10

# Default settings
settings = {
    "DetectType": "motion",
    "BoxType": "all",
    "ReportMedium": "None",
    "ReportType": "None",
    "ReportFreq": "None",
    "FromTime": "None",
    "ToTime": "None",
    "BlackAndWhite": "off",
    "ReduceRes": "off",
    "everyXMinutes": 1000,
    "ReportTo": "dragonslash42@gmail.com"
}

# HTML does not post unticked boxes
# So if the following aren't in the post, disable the setting
checkBoxKeys = ["ReduceRes", "BlackAndWhite"]


@app.route("/")
def index():
    # Return the rendered template
    return render_template("test2.html")


def detection():
    # Grab global references to video stream output and lock
    global vs, outputFrame, lock, box, md

    total = 0
    lastSent = 0

    # Loop over frames from video stream
    while True:
        # Get next frame
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # Timestamp frame
        currentTime = datetime.datetime.now()
        cv2.putText(frame, currentTime.strftime(
                "%d/%m/%y, %H:%M:%S"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 255, 0), 1)

        # Get detections
        (frame, detections) = md.detect(frame)

        if detections is None:
            continue

        if settings["BoxType"] == "all":
            box = detections
            for detect in detections:
                (x, y, w, h) = detect
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        elif (settings["BoxType"] == "merge" or settings["BoxType"] == "none") and len(detections) > 0:
            lowestX = 1000
            lowestY = 1000
            maxWidth = 0
            maxHeight = 0
            for detect in detections:
                (x, y, w, h) = detect
                lowestX = min(lowestX, x)
                lowestY = min(lowestY, y)
                maxWidth = max(maxWidth, x+w)
                maxHeight = max(maxHeight, y+h)
            box = (lowestX, lowestY, maxWidth, maxHeight)
            if settings["BoxType"] == "merge":
                cv2.rectangle(frame, (lowestX, lowestY), (maxWidth, maxHeight), (0, 0, 255), 2)

        # Timer Reporting
        if settings["ReportFreq"] == "timer":
            if(time.time() - lastSent > settings["everyXMinutes"] * 60):
                lastSent = time.time()
                reporter.send(frame, settings["ReportTo"])
                print("Reported to ", settings["ReportTo"])


        # Acquire lock, set output frame and release lock
        with lock:
            outputFrame = frame.copy()


def generate():
    global outputFrame, lock

    while True:
        with lock:
            # Check output frame is available, otherwise skip
            if outputFrame is None:
                # print("No frame")
                continue

            # Encode frame as jpg
            (flags, jpgImage) = cv2.imencode(".jpg", outputFrame)

            # Ensure frame was successfully endoded
            if not flags:
                continue

        # Yield encoded jpg as bytes
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(jpgImage) + b'\r\n')


def getBoxes():
    global box
    while True:
        yield box

@app.route("/video_feed")
def video_feed():
    # return the response generated along with specific media type
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# Returns the most recent frame
@app.route("/single.jpg")
def single():
    global outputFrame, lock
    with lock:
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        return Response(bytearray(encodedImage), mimetype="image/jpg")


# Returns the most recent frame as base64 string
@app.route("/base64")
def getBase64():
    global outputFrame, lock
    with lock:
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        b64String = base64.b64encode(encodedImage)
        return Response(b64String, mimetype="text")


@app.route("/boxes")
def boxes():
    global box
    return Response(str(box), mimetype="text")


@app.route("/settings")
def getSettings():
    global settings, lock
    return jsonify(settings)


# Deal with form request to change parameters
@app.route('/submit', methods=['GET', 'POST'])
def handle_request():
    global settings, md, reporter
    if(request.form["DetectType"] != settings["DetectType"]):
        newType = request.form["DetectType"]
        if newType == "motion":
            md = Motion()
        elif newType == "hog":
            md = HOG()
        elif newType == "bgsub":
            md = BackgroundSubtraction(accumWeight=0.1)
        elif newType == "YOLO":
            md = YOLO()


    if("ReportMedium" in request.form.keys() and request.form["ReportMedium"] != settings["ReportMedium"]):
        if(request.form["ReportMedium"] == "email"):
            reporter = EmailReporter()
        elif(request.form["ReportMedium"]) == "twitter":
            reporter = TwitterReporter()
        

    updateSettings(request.form)
    return redirect("/")
    return index()


# TODO async locks
# TODO Do I even need to save settings here? Maybe put all this in VisionAlgorithm
# And when clientside js requests it send it from the algo
def updateSettings(form):
    global settings, checkBoxKeys
    print(form)

    if not form:
        print("No form submitted...")
        return

    for key, value in form.items():
        # print("Key: ", key, " value: ", value)

        # Invalid key
        if key not in settings:
            print("Invalid setting key!?")
            continue

        if value:
            print("Updating ", key)
            settings[key] = value
            md.updateSetting(key, value)

    # Handles case of check boxes not being posted if off
    for checkBoxKey in checkBoxKeys:
        if checkBoxKey not in form.keys():
            print("Updating checkbox key! ", checkBoxKey)
            settings[checkBoxKey] = "off"
            md.updateSetting(checkBoxKey, "off")

    if isinstance(settings["everyXMinutes"], str):
        settings["everyXMinutes"] = int(settings["everyXMinutes"])

    return

#TODO 
# Deal with form request to change parameters
@app.route('/count')
def getCount():
    global count, lock
    with lock:
        return len(box)


# If main
if __name__ == '__main__':
    # Construct the argument parser and parse command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--ip", type=str, required=True,
                    help="desired ip to run the server on")
    argParser.add_argument("-o", "--port", type=int, required=True,
                    help="desired port to run the server on [1024-65535]")
    args = vars(argParser.parse_args())

    t = threading.Thread(target=detection)
    t.daemon = True
    t.start()

    # Start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

vs.stop()
