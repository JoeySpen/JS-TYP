import numpy as np
import cv2
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class Motion(VisionAlgorithm):

    def __init__(self):
        super().__init__()
        print("Initialising Motion")
        self.prev = None
        self.minSize = 900
        self.settings["BlackAndWhite"] = False
        #self.dontChange["BlackAndWhite"] = True

    def update(self, image):
        return None

    def detect(self, image):
        newImage = super().detect(image)
        if self.prev is None:
            self.prev = newImage
            return
        diff = cv2.absdiff(self.prev, newImage)
        self.prev = newImage.copy()
        # frame1 = image.copy()
        graydiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(graydiff, (5, 5), 0)

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

    # Clears prev frame upon changing a setting
    def updateSetting(self, settingName, settingValue):
        super().updateSetting(settingName, settingValue)
        self.prev = None
