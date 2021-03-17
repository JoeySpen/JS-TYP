import numpy as np
import cv2
import imutils
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class HOG(VisionAlgorithm):

    def __init__(self):
        super().__init__()
        print("Initialising HOG")
        self.name = "HOG"
        # winSize = (32,32) #default
        # winSize = (cap.get(3), cap.get(4)) #joeytest
        # print("winsize: ", winSize)
        # blockSize = (16,16) #default (16,16)
        # blockStride = (8,8) #default 8,8
        # cellSize = (8, 8) #default 8,8
        # nbins = 9 #Number of bins used in calculation of histogram gradients. Default 9
        # derivAperture = 1 #Not documented... default 1
        # winSigma = -1 #Gausian smoothing window parameter, default -1
        # histogramNormType = 0  #??? default 0?
        # L2HysThreshold = 0.2 #l2 normalization method shrinkage default 0.2
        # gammaCorrection = 1 #Flag to specify whether the gamma correction preprocessing is required or not. Default false?
        # nlevels = 64  #Maximum number of detection window increases. Default 64
        # signedGradients = True # Indicates signed gradient will be used or not.  Default false?

        #hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma, histogramNormType, L2HysThreshold, gammaCorrection, nlevels, signedGradients)
        #hog = cv2.HOGDescriptor() #Default settings
        # self.hog = cv2.HOGDescriptor((64,128), (16,16), (8,8), (8,8), 9, 1 ) #Equivalent to default
        self.hog = cv2.HOGDescriptor()
        #hog = cv2.HOGDescriptor((32,64), (8,8), (4,4), (4,4), 9) #This worked well when I didn't resize the image, (half original params), better to make image 2x size?

        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.resizeHeight = 0
        #hog.setSVMDetector(cv2.HOGDescriptor_getDaimlerPeopleDetector())
    
    def update(self, image):
        return None

    def detect(self, image):
        image = super().detect(image)
        #gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        #frame1 = cv2.resize(frame1, (400, 400))
        # image = cv2.resize(image,(480*2,360*2),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        # image = cv2.resize(image, (500, 500))
        boxes, weights = self.hog.detectMultiScale(image, winStride=(2, 2),
                                                   padding=(1, 1), scale=4)
        return image, boxes

    # https://www.researchgate.net/publication/259930836_Improving_HOG_with_Image_Segmentation_Application_to_Human_Detection
    def isHuman(self, image):
        scale = 1
        #resizedImage = cv2.resize(image, (int(64*scale), int(128*scale)), interpolation=cv2.INTER_CUBIC)
        resizedImage = cv2.resize(image, (int(64*scale), int(128*scale)), interpolation=cv2.INTER_AREA)
        # resizedImage = imutils.resize(image, width=min(1200, image.shape[1]))
        #resizedImage = cv2.resize(image, (64, 128))
        # resizedImage = image
        # boxes, weights = self.hog.detect(resizedImage)
        # boxes, weights = self.hog.detectMultiScale(resizedImage, winStride=(4, 4), padding=(8, 8), scale=1.03)
        # Corners? :)

        # Changing winStride helped ALOT here
        # (rects, weights) = self.hog.detect(resizedImage)
        # (rects, weights) = self.hog.detectMultiScale(image, winStride=(1, 1), padding=(8, 8), scale=1.05) #works... OK ish
        (rects, weights) = self.hog.detectMultiScale(resizedImage, winStride=(2, 2), padding=(8, 8), scale=1) #works... OK ish my fave
        # (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        #print("compute:", self.hog.compute(resizedImage), "compute end")

        # compute = self.hog.compute(resizedImage)

        print(rects)
        print(weights)
        
        # help(cv2.HOGDescriptor())

        if(len(rects) > 0):
            print("Its human!")
            for (x, y, w, h) in rects:
                cv2.rectangle(resizedImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print("added")
        else:
            print("None found")


        cv2.imshow("HOG ishuman", resizedImage)
        cv2.waitKey(0)

    # Converts the size of the image based off the person size
    # 0.1 0.5 1 for example
    def setDetectSize(self, personSize):
        self.resizeHeight = 128/personSize




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
