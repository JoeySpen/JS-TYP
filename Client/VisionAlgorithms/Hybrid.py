import numpy as np
import cv2


class Hybrid:

    def __init__(self):
        print("Initialising Hybrid")
        self.prev = None
        self.minSize = 900
        self.HOG = HOG()

    def update(self):
        return

   def detect(self, image):
        if self.prev is None:
            self.prev = image
            return
        diff = cv2.absdiff(self.prev, image)
        self.prev = image.copy()
        # frame1 = image.copy()
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Get thresh and dilate
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Get contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None

        detections = []

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            rect = cv2.boundingRect(contour)
            detections.append(rect)

        return detections
