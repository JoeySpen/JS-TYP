import numpy as np
import cv2


class HOG:

    def __init__(self):
        print("Initialising HOG")
        winSize = (32,32) #default
        #winSize = (cap.get(3), cap.get(4)) #joeytest
        print("winsize: ", winSize)
        blockSize = (16,16) #default (16,16)
        blockStride = (8,8) #default 8,8
        cellSize = (8, 8) #default 8,8
        nbins = 9 #Number of bins used in calculation of histogram gradients. Default 9
        derivAperture = 1 #Not documented... default 1
        winSigma = -1 #Gausian smoothing window parameter, default -1
        histogramNormType = 0  #??? default 0?
        L2HysThreshold = 0.2 #l2 normalization method shrinkage default 0.2
        gammaCorrection = 1 #Flag to specify whether the gamma correction preprocessing is required or not. Default false?
        nlevels = 64  #Maximum number of detection window increases. Default 64
        signedGradients = True # Indicates signed gradient will be used or not.  Default false?

        #hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma, histogramNormType, L2HysThreshold, gammaCorrection, nlevels, signedGradients)
        #hog = cv2.HOGDescriptor() #Default settings
        self.hog = cv2.HOGDescriptor((64,128), (16,16), (8,8), (8,8), 9, 1 ) #Equivalent to default
        #hog = cv2.HOGDescriptor((32,64), (8,8), (4,4), (4,4), 9) #This worked well when I didn't resize the image, (half original params), better to make image 2x size?

        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        #hog.setSVMDetector(cv2.HOGDescriptor_getDaimlerPeopleDetector())
    
    def update(self, image):
        return None

    def detect(self, image):
        #gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        #frame1 = cv2.resize(frame1, (400, 400))
        boxes, weights = self.hog.detectMultiScale(image, winStride=(4, 4),
                                                   padding=(1, 1), scale=4)

        #boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        #print(len(boxes))
        #print("Boxes:\n", boxes)
        return boxes

        #Corners? :)
        #for(xA, yA, xB, yB) in boxes:
           # cv2.rectangle(frame1, (xA, yA), (xB, yB), (0, 255, 0), 2)


        #frame1 = cv2.resize(frame1,(480*2,360*2),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)


#cap = cv2.VideoCapture('vtest.avi.mp4')
#frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
#out = cv2.VideoWriter('output.avi', fourcc, 5.0, (1280, 720))

#ret, frame1 = cap.read()
#frame1 = cv2.resize(frame1,(480*2,360*2),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)



# while cap.isOpened():
#   #gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
#   #frame1 = cv2.resize(frame1, (400, 400))
#   boxes, weights = hog.detectMultiScale(frame1, winStride=(4, 4),
# 		padding=(1, 1), scale=4)
#   boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
#   #print(len(boxes))
#   #print("Boxes:\n", boxes)

#   #Corners? :)
#   for(xA, yA, xB, yB) in boxes:
#     cv2.rectangle(frame1, (xA, yA), (xB, yB), (0, 255, 0), 2)

#   out.write(frame1.astype('uint8'))


#   cv2.imshow("HOG", frame1)
#   cv2.waitKey(0)



#   ret, frame1 = cap.read()
#   frame1 = cv2.resize(frame1,(480*2,360*2),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
