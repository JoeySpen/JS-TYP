# import the necessary packages
import numpy as np
import imutils
import cv2
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class SingleMotionDetector(VisionAlgorithm):
    def __init__(self, accumWeight=0.5):
        super().__init__()
        # store the accumulated weight factor
        self.name = "BG Sub"
        self.accumWeight = accumWeight
        # initialize the background model
        self.bg = None

    def update(self, image):
        # If background is none initialize it
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image):
        clean = super().detect(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.update(image)
        # Difference between background and frame
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Remove noise
        thresh = cv2.erode(thresh, None, iterations=2)
        dilated = cv2.dilate(thresh, None, iterations=2)

        # Get contours
        contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        detections = []

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            rect = cv2.boundingRect(contour)
            detections.append(rect)

        return clean, detections
