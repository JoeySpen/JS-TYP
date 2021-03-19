import numpy as np
import cv2
import imutils
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class HOG(VisionAlgorithm):

    def __init__(self):
        super().__init__()
        print("Initialising HOG")
        self.name = "HOG"
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.resizeHeight = 0
    
    def update(self, image):
        return None

    def detect(self, image):
        image = super().detect(image)
        boxes, weights = self.hog.detectMultiScale(image, winStride=(2, 2),
                                                   padding=(1, 1), scale=4)
        return image, boxes

    def isHuman(self, image):
        scale = 1
        resizedImage = cv2.resize(image, (int(64*scale), int(128*scale)), interpolation=cv2.INTER_AREA)
        (rects, weights) = self.hog.detectMultiScale(resizedImage, winStride=(2, 2), padding=(8, 8), scale=1) #works... OK ish my fave

        print(rects)
        print(weights)

        if(len(rects) > 0):
            print("Its human!")
            for (x, y, w, h) in rects:
                cv2.rectangle(resizedImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print("added")
            return True
        else:
            return False

    # Converts the size of the image based off the person size
    # 0.1 0.5 1 for example
    def setDetectSize(self, personSize):
        self.resizeHeight = 128/personSize
