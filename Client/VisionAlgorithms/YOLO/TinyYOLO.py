from VisionAlgorithms.YOLO.YOLO import YOLO
import cv2


class TinyYOLO(YOLO):
    def __init__(self):
        super().__init__()
        self.name = "Tiny YOLO"
        self.cfgLoc = "VisionAlgorithms/YOLO/tinyyolo-coco/yolov3-tiny.cfg"
        self.weightsLoc = "VisionAlgorithms/YOLO/tinyyolo-coco/yolov3-tiny.weights"
        

        print("Attempting to load TinyYOLO...")
        self.neuralNet = cv2.dnn.readNetFromDarknet(self.cfgLoc, self.weightsLoc)

        #(H, W) = frame1.shape[:2]

        # Get output layer names we need from YOLO
        self.ln = self.neuralNet.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.neuralNet.getUnconnectedOutLayers()]

        #self.settings["BlackAndWhite"] = False
        #self.dontChange["BlackAndWhite"] = True   
    
    def updateSetting(self, settingName, settingValue):
        super().updateSetting(settingName, settingValue)
        if(self.settings["BlackAndWhite"]):
            self.cfgLoc = "VisionAlgorithms/YOLO/tinyyolo-coco/yolov3-tinybw.cfg"
            self.neuralNet = cv2.dnn.readNetFromDarknet(self.cfgLoc, self.weightsLoc)