from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG

HOG = HOG()
img = cv2.imread('image/4n.png')

HOG.isHuman(img)