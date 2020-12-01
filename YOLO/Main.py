import numpy as np
import cv2
import time

cap = cv2.VideoCapture('vtest.mp4')                 #Video capture
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter('output.avi', fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()

#Locations and parameters
labelsLocation = "yolo-coco\coco.names"
cfgLocation = "yolo-coco\yolov3.cfg"
weightsLocation = "yolo-coco\yolov3.weights"
confidenceMin = 0.5
thresholdMin = 0.3

#Load the labels
LABELS = open(labelsLocation).read().strip().split("\n")

#Get random colours for labels
np.random.seed(100)
COLORS = np.random.randint(0, 225, size=(len(LABELS), 3), dtype="uint8")

print("Attempting to load YOLO...")
net = cv2.dnn.readNetFromDarknet(cfgLocation, weightsLocation)

(H,W) = frame1.shape[:2]

#Get output layer names we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] -1] for i in net.getUnconnectedOutLayers()]



while cap.open:
  #Construct a blob from the input and perform forward pass of object detector giving us bounding boxes and probabilities
  blob = cv2.dnn.blobFromImage(frame1, 1 / 255.0, (416, 416), swapRB=True, crop=False)
  net.setInput(blob)
  start = time.time()
  layerOutputs = net.forward(ln)
  end = time.time()
  end = end - start

  print("Yolo took ", end, " seconds")

  boxes = []
  confidences = []
  classIDs = []

  for output in layerOutputs:
    for detection in output:
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]

      if confidence > confidenceMin:
        box = detection[0:4] * np.array([W, H, W, H]) 
        (centerX, centerY, width, height) = box.astype("int")

        x = int(centerX - (width/2))
        y = int(centerY - (height/2))

        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))
        classIDs.append(classID)

  idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidenceMin, thresholdMin)


  #Draw to image
  if len(idxs) > 0:
    for i in idxs.flatten():
      # extract the bounding box coordinates
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])

      # draw a bounding box rectangle and label on the image
      color = [int(c) for c in COLORS[classIDs[i]]]
      cv2.rectangle(frame1, (x, y), (x + w, y + h), color, 2)
      text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
      cv2.putText(frame1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

  cv2.imshow("Image", frame1)
  cv2.waitKey(0)
  ret, frame1 = cap.read()

