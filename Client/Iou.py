from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO
from VisionAlgorithms.YOLO.TinyYOLO import TinyYOLO
from VisionAlgorithms.BackgroundSubtraction import BackgroundSubtraction
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

# Draws detection to frame in specified colour
def draw(detections, frame, colour):
    if detections is None:
        return

    for detect in detections:
        (x, y, w, h) = detect
        cv2.rectangle(frame, (x, y), (x+w, y+h), colour, 2)


# Algorithms to test
mvAlgos = [TinyYOLO()]

# Algorithm we are testing against
YOLO = YOLO()

# Vid setup
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None
frameCount = 0

# Colour setup
np.random.seed(1000)
yoloColour = (0, 0, 255)
testColour = (0, 255, 0)
testColours = np.random.randint(0, 225, size=(len(mvAlgos), 3), dtype="uint8")

print("Colours:", testColours[0])


testVid.release()
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None

results = []

for algo in mvAlgos:
    results.append([])

print(results)

while True:
    ret, frame = testVid.read()
    # frame = cv2.resize(frame,(480*2,360*2),fx=0,fy=0, interpolation = cv2.INTER_CUBIC) #Required for HOG detection
    frameCount += 1

    # Frames to measure
    if frameCount > 100:
        break

    # End of video
    if not ret:
        print("End of video")
        break

    cleanFrame = frame.copy()
    frame, yoloDetections = YOLO.detect(frame)
    draw(yoloDetections, frame, yoloColour)

    frameResults = [None] * len(mvAlgos)
    algoNum = 0

    # Get detections for each test algorithm
    for algo in mvAlgos:
        unusedFrame, detections = algo.detect(cleanFrame)

        if detections is None or yoloDetections is None:
            continue

        # Draw detections in this algos colour
        color = (int(testColours[algoNum][0]), int(testColours[algoNum][1]),
                 int(testColours[algoNum][2]))
        draw(detections, frame, color)

        # Put 0s for every failed detection
        frameResults[algoNum] = [0] * max(len(detections), len(yoloDetections)) 
        detectionNum = 0

        # Find score for each detection
        if len(detections) > 0:
            for box in detections:
                # best.append(0)
                for yolobox in yoloDetections:
                    frameResults[algoNum][detectionNum] = max(frameResults[algoNum][detectionNum],
                                                  getIOU(box, yolobox))
                detectionNum += 1

            # Calculate the score (average) for this specific frame
            frameAverage = sum(frameResults[algoNum])/len(frameResults[algoNum])
            # print("Results for this frame: ", frameAverage)
            
            # Average of this frame is added to final result
            results[algoNum].append(frameAverage)
        algoNum += 1
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)

print("Results:\n", results)


for i, algo in enumerate(mvAlgos):
    # Average of each frame is taken for final score
    totalScore = sum(results[i])/len(results[i])
    print("Final score for ", mvAlgos[i].name, "is: ", totalScore)

testVid.release()
