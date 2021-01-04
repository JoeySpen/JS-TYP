import numpy as np
import cv2


class Motion:

    def __init__(self, accumWeight=0.5):
        print("Initialising Motion")
        self.prev = None
        self.minSize = 900

    def update(self, image):
        return None

    def detect(self, image):
        if self.prev is None:
            self.prev = image
            return
        diff = cv2.absdiff(self.prev, image)
        self.prev = image.copy()
        #frame1 = image.copy()
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

            

        #(minX, minY) = (np.inf, np.inf)
        #maxX, maxY = (-np.inf, -np.inf)

        if len(contours) == 0:
            return None

        return contours
        

        # Otherwise loop over contours
        #for c in contours:
            # Compute bounding box of contour and use it to update min
            # and maximum bounding regions
            #(x, y, w, h) = cv2.boundingRect(c)
            #(minX, minY) = (min(minX, x), min(minY, y))
            #(maxX, maxY) = (max(maxX, x+w)), max(maxY, y+h)

        # Otherwise return a tuple of the thresholded image
        # along with bounding box
        #return (thresh, (minX, minY, maxX, maxY))

        #return contours
            #cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #'cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), 
                        #cv2.FONT_HERSHEY_SIMPLEX,
                        #1, (0, 0, 255), 3)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        #image = cv2.resize(frame1, (1280, 720))
        #out.write(image)
        #cv2.imshow("feed", frame1)
        #frame1 = frame2
        #ret, frame2 = cap.read()

        #if cv2.waitKey(40) == 27:
            #break



    #print("Loading...")
    # cap = cv2.VideoCapture('vtest.avi.mp4')                 #Video capture
    #cap = cv2.VideoCapture(0)
    #frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

    # out = cv2.VideoWriter('output.avi', fourcc, 5.0, (1280,720))

    #ret, frame1 = cap.read()
    #ret, frame2 = cap.read()
    #p rint(frame1.shape)
    #while cap.isOpened():
        

    #cv2.destroyAllWindows()
    #cap.release()
    #out.release()