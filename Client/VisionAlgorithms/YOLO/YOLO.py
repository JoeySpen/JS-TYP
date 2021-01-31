import numpy as np
import cv2
import time


class YOLO:

    def __init__(self):
        print("Initialising YOLO")
        self.prev = None
        self.labelsLocation = "VisionAlgorithms/YOLO/yolo-coco/coco.names"
        self.cfgLocation = "VisionAlgorithms/YOLO/yolo-coco/yolov3.cfg"
        self.weightsLocation = "VisionAlgorithms/YOLO/yolo-coco/yolov3.weights"
        self.confidenceMin = 0.5
        self.thresholdMin = 0.3

        # Load the labels
        self.LABELS = open(self.labelsLocation).read().strip().split("\n")

        # Get random colours for labels
        np.random.seed(100)
        self.COLORS = np.random.randint(0, 225, size=(len(self.LABELS), 3), dtype="uint8")

        print("Attempting to load YOLO...")
        self.net = cv2.dnn.readNetFromDarknet(self.cfgLocation, self.weightsLocation)

        #(H, W) = frame1.shape[:2]

        # Get output layer names we need from YOLO
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def update(self, image):
        return None

    def detect(self, frame1):

        (H, W) = frame1.shape[:2]

        blob = cv2.dnn.blobFromImage(frame1, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        end = end - start

        #print("Yolo took ", end, " seconds")

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.confidenceMin:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    x = int(centerX - (width/2))
                    y = int(centerY - (height/2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidenceMin, self.thresholdMin)

        print(idxs)
        result = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                result.append(boxes[i])
        return result

        # Draw to image
        if len(idxs) > 0:
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(frame1, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
