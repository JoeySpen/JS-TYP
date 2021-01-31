from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO


def getIOU(box1, box2):
    xOverlap = max(min(box1[2], box2[2] - max(box1[0], box2[0])))
    yOverlap = max(min(box1[3], box2[3] - max(box1[1], box2[1])))
    overlapArea = xOverlap * yOverlap
    return overlapArea


def draw(detections, frame, colour):
    if detections is None:
        return

    for detect in detections:
        (x, y, w, h) = detect
        cv2.rectangle(frame, (x, y), (x+w, y+h), colour, 2)


mvAlgos = [Motion(), HOG()]
YOLO = YOLO()
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None
frameCount = 0

yoloColour = (0, 0, 255)
testColour = (0, 255, 0)

for algo in mvAlgos:
    testVid.release()
    testVid = cv2.VideoCapture('testVids/vtest.mp4')
    frame = None
    frameCount = 0
    print("Testing algorithm...")
    startTime = datetime.now()

    while True:
        ret, frame = testVid.read()

        # End of video
        if not ret:
            print("Done")
            endTime = datetime.now()
            elapsedTime = endTime - startTime
            print("Elapsed time:", elapsedTime,
                  "\tframes processed: ", frameCount)
            break

        #detections = algo.detect(frame)
        yoloDetections = YOLO.detect(frame)
        #draw(detections, frame, testColour)
        draw(yoloDetections, frame, yoloColour)
        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        frameCount += 1

testVid.release()
