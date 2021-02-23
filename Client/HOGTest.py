from datetime import datetime
import cv2
from VisionAlgorithms.Motion import Motion
from VisionAlgorithms.HOG import HOG

HOG = HOG()
img = cv2.imread('image/3.png')

for i in range(1, 9):
    img = cv2.imread('image/' + str(i) + '.png')
    HOG.isHuman(img)

for i in range(1, 9):
    img = cv2.imread('image/' + str(i) + 'n.png')
    HOG.isHuman(img)

