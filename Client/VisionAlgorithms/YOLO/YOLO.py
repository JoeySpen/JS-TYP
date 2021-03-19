import numpy as np
import cv2
from VisionAlgorithms.VisionAlgorithm import VisionAlgorithm


class YOLO(VisionAlgorithm):

    def __init__(self):
        super().__init__()
        print("Initialising YOLO")

        self.name = "YOLO"
        self.backends = (cv2.dnn.DNN_BACKEND_DEFAULT, cv2.dnn.DNN_BACKEND_HALIDE, cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE, cv2.dnn.DNN_BACKEND_OPENCV)
        self.targets = (cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_OPENCL, cv2.dnn.DNN_TARGET_OPENCL_FP16, cv2.dnn.DNN_TARGET_MYRIAD)
        self.prev = None
        self.labelLoc = "VisionAlgorithms/YOLO/yolo-coco/coco.names"
        # self.cfgLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3bw.cfg"
        self.cfgLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3.cfg"
        self.weightsLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3.weights"
        self.confMin = 0.5
        self.thresMin = 0.3
        #self.settings["BlackAndWhite"] = True
        #self.dontChange["BlackAndWhite"] = True     # TODO better black and white toggle...

        # Load the labels
        self.labels = open(self.labelLoc).read().strip().split("\n")

        # Get random colours for labels
        np.random.seed(100)
        self.colours = np.random.randint(0, 225, size=(len(self.labels), 3), dtype="uint8")

        self.neuralNet = cv2.dnn.readNetFromDarknet(self.cfgLoc, self.weightsLoc)

        # Layer names
        self.ln = self.neuralNet.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.neuralNet.getUnconnectedOutLayers()]

        self.peopleOnly = True

    def update(self, image):
        return None

    def detect(self, image):
        image = super().detect(image)

        (H, W) = image.shape[:2]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), crop=False)
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

                    # Add box confidences and ID
                    boxes.append([x, y, int(bWidth), int(bHeight)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confMin, self.thresMin)

        result = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                result.append(boxes[i])
        return image, result

        # Draw to image
        if len(idxs) > 0:
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.colours[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Clears prevImage frame upon changing a setting
    def updateSetting(self, settingName, settingValue):
        super().updateSetting(settingName, settingValue)
        if(self.settings["BlackAndWhite"]):
            self.cfgLoc = "VisionAlgorithms/YOLO/yolo-coco/yolov3bw.cfg"
            self.neuralNet = cv2.dnn.readNetFromDarknet(self.cfgLoc, self.weightsLoc)
