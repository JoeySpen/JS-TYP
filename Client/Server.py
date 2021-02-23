from SingleMotionDetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
from copy import deepcopy
from flask import request
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO
from OpenSSL import SSL
# from DiscordReporter import DiscordReporter

# python Server.py --ip 192.168.56.1 --port 8000
# python Server.py --ip 127.0.0.1 --port 8000
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

# Initialize the video stream and allow camera to warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
# vs = cv2.VideoCapture(0)
time.sleep(1)

t = None

md = Motion()

discordReporter = None

# Algo settings
minSize = 0
maxSize = 100
boxType = None

count = 0

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
    "ReduceRes": "off"
}

# HTML does not post unticked boxes
# So if these aren't in the post, disable the setting
checkBoxKeys = ["ReduceRes", "BlackAndWhite"]


@app.route("/")
def index():
    # Return the rendered template
    return render_template("test2.html")


def detectMotion(frameCount):
    # Grab global references to video stream output and lock
    global vs, outputFrame, lock, box, md

    # Initialise motion detector and number of frames
    # md = SingleMotionDetector(accumWeight=0.1)
    # md = Motion(accumWeight=0.1)
    # md = Motion()
    total = 0

    # Loop over frames from video stream
    while True:
        # Read next frame from stream, resize convert and blur
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # #TODO Do this stuff in the respective motion technique

        # Grab current timestamp and draw to frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # If total frames sufficient to construct background model
        # Continue to process frame
        if total > frameCount:
            # motion = md.detect(frame)
            detections = md.detect(frame)

            if detections is None:
                continue

            box = detections

            #print(detections)

            for detect in detections:
                (x, y, w, h) = detect
                # box.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            # Check if we found motion
            # if motion is not None:
                # Unpack tuple and draw box surrounding motion area
                # (thresh, (minX, minY, maxX, maxY)) = motion
                # cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                #             (0, 0, 255), 2)
                # box = (minX, minY, maxX, maxY)

        # Update background model and increment total num
        # of frames read thus far
        #md.update(frame)  # md.update(gray) #TODO
        total += 1

        # cv2.imshow("feed", frame)
        # cv2.waitKey(0)

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

@app.route("/settings")
def getSettings():
    return settings

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


@app.route("/boxes")
def boxes():
    global box
    print(box)

    # def generate():
    #     lastBox = None
    #     while True:
    #         global box
    #         if lastBox == box:
    #             break
    #         rsp = '{0[0]},{0[1]},{0[2]},{0[3]}'.format(box)
    #         lastBox = deepcopy(box)
    #         yield rsp
    # val = getBoxes().__next__()
    # global box
    # return Response(rsp, mimetype="text")
    return Response(str(box), mimetype="text")

# Deal with form request to change parameters
@app.route('/submit', methods=['GET', 'POST'])
def handle_request():
    global settings, md
    if(request.form["DetectType"] != settings["DetectType"]):
        newType = request.form["DetectType"]
        if newType == "motion":
            md = Motion()
        elif newType == "hog":
            md = HOG()
        elif newType == "bgsub":
            md = SingleMotionDetector(accumWeight=0.1)
        elif newType == "YOLO":
            md = YOLO()

    updateSettings(request.form)

    #print("form: ", request.form)
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
        print("Key: ", key, " value: ", value)

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
            md.updateSetting(key, "off")

    return

# Deal with form request to change parameters
@app.route('/count', methods=['GET', 'POST'])
def getCount():
    global count, lock
    with lock:
        return count


# If main
if __name__ == '__main__':
    # Construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of server (1024, to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct background model")
    args = vars(ap.parse_args())

    # Start a thread that will perform motion detection
    t = threading.Thread(target=detectMotion, args=(args["frame_count"],))
    t.daemon = True
    t.start()

    # Start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

vs.stop()
