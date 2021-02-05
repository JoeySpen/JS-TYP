from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO
import numpy as np


def getIOU(box1, box2):
    # Determine the (x, y) coordinates of the intersection...

    # Convert from (x, y, w, h) to (x1, y1, x2, y2)
    boxA = (box1[0], box1[1], box1[0]+box1[2], box1[1] + box1[3])
    boxB = (box2[0], box2[1], box2[0]+box2[2], box2[1] + box2[3])

    # Box = (x1, y1, x2, y2)

    # Top left corner
    x1 = max(boxA[0], boxB[0])
    y1 = max(boxA[1], boxB[1])

    # Bottom right corner
    x2 = min(boxA[2], boxB[2])
    y2 = min(boxB[3], boxB[3])

    # 0 is incase they do not interesct!
    intersectionArea = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    # Determine union
    areaA = abs((boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1))
    areaB = abs((boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1))

    union = (areaA + areaB) - intersectionArea

    iou = intersectionArea / union

    return iou


def draw(detections, frame, colour):
    if detections is None:
        return

    for detect in detections:
        (x, y, w, h) = detect
        cv2.rectangle(frame, (x, y), (x+w, y+h), colour, 2)


# Main
mvAlgos = [HOG(), Motion()]
names = ["HOG", "Motion"]
YOLO = YOLO()
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None
frameCount = 0

np.random.seed(1000)
yoloColour = (0, 0, 255)
testColour = (0, 255, 0)
testColours = np.random.randint(0, 225, size=(len(mvAlgos), 3), dtype="uint8")

print(testColours[0])


testVid.release()
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None

while True:
    ret, frame = testVid.read()
    cleanFrame = frame.copy()

    # End of video
    if not ret:
        print("End of video")
        break

    yoloDetections = YOLO.detect(frame)
    draw(yoloDetections, frame, yoloColour)

    results = [None] * len(mvAlgos)
    algoNum = 0

    for algo in mvAlgos:
        detections = algo.detect(cleanFrame)

        if detections is None or yoloDetections is None:
            continue

        # Draw detections in this algos colour
        color = (int(testColours[algoNum][0]), int(testColours[algoNum][1]), 
                 int(testColours[algoNum][2]))
        draw(detections, frame, color)

        results[algoNum] = [0] * max(len(detections), len(yoloDetections))
        count = 0
        if len(detections) > 0:
            for box in detections:
                # best.append(0)
                for yolobox in yoloDetections:
                    results[algoNum][count] = max(results[algoNum][count],
                                                  getIOU(box, yolobox))
                count += 1

        algoNum += 1

        for i, algo in enumerate(mvAlgos):
            print(names[i], results[i])

    cv2.imshow("frame", frame)
    cv2.waitKey(1)

testVid.release()
