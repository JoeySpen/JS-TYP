import numpy as np
import cv2


def overlap(currentBox, previousBox):
    #print("Im comparing ", currentBox, " and ", previousBox)
    if currentBox[0] < previousBox[0]+ previousBox[2] and currentBox[0] + currentBox[2] > previousBox[0] and currentBox[1] < previousBox[1] + previousBox[3] and currentBox[1] + currentBox[3] > previousBox[1]:
        return True
    else:
        return False

cap = cv2.VideoCapture('vtest.avi.mp4')                 #Video capture
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter('output.avi', fourcc, 5.0, (1280,720))

ret, prevFrame = cap.read()
ret, currFrame = cap.read()

previousBoxes = []

#HOG
hog = cv2.HOGDescriptor((64,128), (16,16), (8,8), (8,8), 9, 1 ) #Equivalent to default
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#For each frame
while cap.isOpened():
    cleanFrame = currFrame.copy()

    diff = cv2.absdiff(prevFrame, currFrame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    cv2.waitKey(0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    currentBoxes = []

    #For each countour
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 900:
            cv2.rectangle(currFrame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            currentBoxes.append(cv2.boundingRect(contour))

    #Handle case of first frame or no prev boxes
    count = 0
    if previousBoxes:
        #Compare previous and current boxes...
        for previousBox in previousBoxes:
            matched = False
            for currentBox in currentBoxes:
                count+=1
                if overlap(currentBox, previousBox):
                    matched = True

            #No match, did someone stand still?
            if not matched:
                (x, y, w, h) = previousBox
                #cv2.rectangle(currFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                slicedImage = cleanFrame[y:y+h, x:x+w]
                slicedResize = cv2.resize(slicedImage,(64,128),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

                #Check for HOG within this previous box
                boxes, weights = hog.detectMultiScale(cleanFrame, winStride=(4, 4), padding=(1, 1), scale=4)
                boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
                print("Hog found ", len(boxes) ," boxes")
                if(len(boxes) > 0):
                    cv2.rectangle(currFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    currentBoxes.append(previousBox)

                #for(xA, yA, xB, yB) in boxes:
                    #cv2.rectangle(slicedResize, (xA, yA), (xB, yB), (255, 255, 0), 2)

                cv2.imshow("Sliced Image", slicedResize)
                

    #print("Count: ", count)

    #Resize and show image
    #image = cv2.resize(frame1, (1280,720))
    #out.write(image)
    cv2.imshow("Hybrid method", currFrame)

    #Progressing frames
    prevFrame = cleanFrame
    ret, currFrame = cap.read()

    #Progressing boxes
    previousBoxes = currentBoxes

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()

