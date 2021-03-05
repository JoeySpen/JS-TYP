# import the necessary packages
import numpy as np
import imutils
import cv2


class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
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

    def detect(self, image, tVal=25):
        # Compute abs difference between background model and iamge passed in
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # Perform series of erosions and dilations to remove small blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours in threshold image and initialize
        # the min and max bounding box regions for motion
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        (minX, minY) = (np.inf, np.inf)
        maxX, maxY = (-np.inf, -np.inf)

        # No contours
        if len(cnts) == 0:
            return None

        # Otherwise loop over contours
        for c in cnts:
            # Compute bounding box of contour and use it to update min
            # and maximum bounding regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x+w)), max(maxY, y+h)

        # Otherwise return a tuple of the thresholded image
        # along with bounding box
        return (thresh, (minX, minY, maxX, maxY))
