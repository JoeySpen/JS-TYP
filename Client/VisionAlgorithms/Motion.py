import numpy as np
import cv2
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class Motion(VisionAlgorithm):

    def __init__(self):
        super().__init__()
        self.name = "Motion"
        print("Initialising Motion")
        self.prevImage = None
        self.minSize = 900
        #self.dontChange["BlackAndWhite"] = True

    def update(self, image):
        return None

    def detect(self, image):
        newImage = super().detect(image)
        if self.prevImage is None:
            self.prevImage = newImage
            return newImage, None
        diff = cv2.absdiff(self.prevImage, newImage)
        self.prevImage = newImage.copy()
        # frame1 = image.copy()
        if not self.settings["BlackAndWhite"]:
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff, (5, 5), 0)

        # Get thresh and dilate
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Get contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return newImage, None

        detections = []

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            rect = cv2.boundingRect(contour)
            detections.append(rect)

        return newImage, detections

    # Clears prevImage frame upon changing a setting
    def updateSetting(self, settingName, settingValue):
        super().updateSetting(settingName, settingValue)
        self.prevImage = None
