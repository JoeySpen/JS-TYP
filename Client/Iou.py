from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO


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

        detections = algo.detect(frame)
        yoloDetections = YOLO.detect(frame)
        draw(detections, frame, testColour)
        draw(yoloDetections, frame, yoloColour)

        if detections is None or yoloDetections is None:
            continue

        #best = 0

        best = []
        count = 0
        if len(detections) > 0:
            for box in detections:
                best.append(0)
                for yolobox in yoloDetections:
                    best[count] = max(best[count], getIOU(box, yolobox))
                count += 1

        print("Best:", best)

        cv2.imshow("frame", frame)
        cv2.waitKey(0)
        frameCount += 1

testVid.release()
