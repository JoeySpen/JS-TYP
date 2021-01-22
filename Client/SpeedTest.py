from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG


# Draws a list of detections to a frame
def draw(detections, frame):
    if detections is None:
        return

    for detect in detections:
        (x, y, w, h) = detect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)


mvAlgos = [Motion(), HOG()]
testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None
frameCount = 0

for algo in mvAlgos:
    testVid.release()
    testVid = cv2.VideoCapture('testVids/vtest.mp4')
    frame = None
    frameCount = 0
    print("Testing algorithm...")
    startTime = datetime.now()

    while True:
        ret, frame = testVid.read()

        if not ret:
            print("Done")
            endTime = datetime.now()
            elapsedTime = endTime - startTime
            print("Elapsed time:", elapsedTime,
                  "\tframes processed: ", frameCount)
            break

        detections = algo.detect(frame)
        # draw(detections, frame)
        # cv2.imshow("frame", frame)
        # cv2.waitKey(1)
        frameCount += 1

testVid.release()

print("Tested ", frameCount, " frames!")
