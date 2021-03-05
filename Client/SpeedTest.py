from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG
from VisionAlgorithms.YOLO.YOLO import YOLO
from VisionAlgorithms.YOLO.TinyYOLO import TinyYOLO


# Draws a list of detections to a frame
def draw(detections, frame):
    if detections is None:
        return

    for detect in detections:
        (x, y, w, h) = detect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)


mvAlgos = [HOG(), HOG(), HOG(), Motion(), Motion(), Motion(), TinyYOLO(), TinyYOLO(), TinyYOLO()]
mvAlgos[1].updateSetting("BlackAndWhite", True)
mvAlgos[2].updateSetting("ReduceRes", True)

mvAlgos[4].updateSetting("BlackAndWhite", True)
mvAlgos[5].updateSetting("ReduceRes", True)

mvAlgos[7].updateSetting("BlackAndWhite", True)
mvAlgos[8].updateSetting("ReduceRes", True)


testVid = cv2.VideoCapture('testVids/vtest.mp4')
frame = None
frameCount = 0
#HOG = HOG()

for algo in mvAlgos:
    testVid.release()
    testVid = cv2.VideoCapture('testVids/vtest.mp4')
    frame = None
    frameCount = 0
    #print("Testing algorithm...")
    startTime = datetime.now()

    while True:
        ret, frame = testVid.read()

        if not ret:
            #print("Done")
            endTime = datetime.now()
            elapsedTime = endTime - startTime
            print(algo.name,
                    "\tElapsed time:", elapsedTime,
                    "\tframes processed: ", frameCount, "\n",
                    algo.settings, "\n")
            break

        frame, detections = algo.detect(frame)

        # HOG test fun
        # if detections:
        #     for detection in detections:
        #         (x, y, w, h) = detection
        #         slicedImage = frame[y:y+h, x:x+w]
        #         HOG.isHuman(slicedImage)
                ##slicedResize = cv2.resize(slicedImage,(64,128),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)



        #draw(detections, frame)
        #cv2.imshow("frame", frame)
        #cv2.waitKey(1)
        frameCount += 1

testVid.release()

#print("Tested ", frameCount, " frames!")
