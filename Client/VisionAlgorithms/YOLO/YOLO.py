import numpy as np
import cv2


class YOLO:

    def __init__(self):
        print("Initialising YOLO")
        self.prev = None
        self.labelLoc = "VisionAlgorithms/YOLO/yolo-coco/coco.names"
        self.cfgLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3.cfg"
        self.weightsLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3.weights"
        self.confMin = 0.5
        self.thresMin = 0.3

        # Load the labels
        self.labels = open(self.labelLoc).read().strip().split("\n")

        # Get random colours for labels
        np.random.seed(100)
        self.colours = np.random.randint(0, 225, size=(len(self.labels), 3), dtype="uint8")

        print("Attempting to load YOLO...")
        self.neuralNet = cv2.dnn.readNetFromDarknet(self.cfgLoc, self.weightsLoc)

        #(H, W) = frame1.shape[:2]

        # Get output layer names we need from YOLO
        self.ln = self.neuralNet.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.neuralNet.getUnconnectedOutLayers()]

        self.peopleOnly = True

    def update(self, image):
        return None

    def detect(self, frame1):

        (H, W) = frame1.shape[:2]

        blob = cv2.dnn.blobFromImage(frame1, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.neuralNet.setInput(blob)
        layerOutputs = self.neuralNet.forward(self.ln)
        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # Skip if not person and set to peopleonly
                if classID != 0 and self.peopleOnly:
                    continue

                # If meets minimum confidence
                if confidence > self.confMin:
                    # Convert from YOLO bounding box to standard X, Y, W, H
                    box = detection[0:4] * np.array([W, H, W, H])
                    (bCentreX, bCentreY, bWidth, bHeight) = box.astype("int")

                    x = int(bCentreX - (bWidth/2))
                    y = int(bCentreY - (bHeight/2))

                    # Add box, confidences and ID
                    boxes.append([x, y, int(bWidth), int(bHeight)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confMin, self.thresMin)

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
                color = [int(c) for c in self.colours[classIDs[i]]]
                cv2.rectangle(frame1, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.labels[classIDs[i]], confidences[i])
                cv2.putText(frame1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
