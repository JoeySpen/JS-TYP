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

# python webstreaming.py --ip 192.168.0.74 --port 8000
# http://camera.butovo.com/mjpg/video.mjpg

# Initialise output frame and a lock to allow
# thread safe exchange of output frames
outputFrame = None
lock = threading.Lock()

# Initialize a flask object
app = Flask(__name__)

# Initialize boxes
box = (0, 0, 0, 0)

# Initialize the video stream and allow camera to warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
# vs = cv2.VideoCapture(0)
time.sleep(1)


@app.route("/")
def index():
    # Return the rendered template
    return render_template("index.html")


def detect_motion(frameCount):
    # Grab global references to video stream output and lock
    global vs, outputFrame, lock, box

    # Initialise motion detector and number of frames
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    # Loop over frames from video stream
    while True:
        # Read next frame from stream, resize convert and blur
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # Grab current timestamp and draw to frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # If total frames sufficient to construct background model
        # Continue to process frame
        if total > frameCount:
            motion = md.detect(gray)

            # Check if we found motion
            if motion is not None:
                # Unpack tuple and draw box surrounding motion area
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)
                box = (minX, minY, maxX, maxY)


        # Update background model and increment total num
        # of frames read thus far
        md.update(gray)
        total += 1

        # cv2.imshow("feed", frame)
        # cv2.waitKey(0)

        # Acquire lock, set output frame and release lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # Grab global references
    global outputFrame, lock

    while True:
        # wait until lock is acquired
        with lock:
            # Check output frame is available, otherwise skip
            if outputFrame is None:
                # print("No frame")
                continue

            # Encode frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # Ensure frame was successfully endoded
            if not flag:
                continue

        # yield output frame in byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


def getBoxes():
    global box
    while True:
        yield box


@app.route("/video_feed")
def video_feed():
    # return the response generated along with specific media type
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/single.jpg")
def single():
    global outputFrame
    (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
    return Response(bytearray(encodedImage), mimetype="image/jpg")


@app.route("/boxes")
def boxes():
    def generate():
        lastBox = None
        while True:
            global box
            if lastBox == box:
                break
            rsp = '{0[0]},{0[1]},{0[2]},{0[3]}'.format(box)
            lastBox = deepcopy(box)
            yield rsp
    # val = getBoxes().__next__()
    # global box
    # return Response(rsp, mimetype="text")
    return Response(generate(), mimetype="text")

# @app.route('/large')
# def generate_large_csv():
#     def generate():
#         for i in range(0,1000000):
#             yield ','.join("bob") + '\n'
#     return Response(generate(), mimetype='text')


# Deal with form request to change parameters
@app.route('/submit', methods=['GET', 'POST'])
def handle_request():
    #print("Got request?")
    print(request.form)
    return index()


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
    t = threading.Thread(target=detect_motion, args=(args["frame_count"],))
    t.daemon = True
    t.start()

    # Start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

vs.stop()
