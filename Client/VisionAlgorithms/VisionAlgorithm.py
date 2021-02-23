import cv2

# Parent class for all Vision Algorithms
class VisionAlgorithm:

    def __init__(self):
        # Load default settings
        self.settings = {
            "BoxType": "all",
            "ReportMedium": None,
            "ReportType": None,
            "ReportFreq": None,
            "FromTime": None,
            "ToTime": None,
            "BlackAndWhite": False,
            "ReduceRes": False
        }

        self.dontChange = {
            
        }

        self.mapSettings = {
            "on": True,
            "off": False,
            "None": None
        }

    def detect(self, image):
        if(self.settings["BlackAndWhite"]):
            #print("b+w")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if(self.settings["ReduceRes"]):
            # print("Reduce res")
            image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)), interpolation=cv2.INTER_AREA)
        return image

    def updateSetting(self, settingName, settingValue):
        if(settingName in self.dontChange.keys()):
            return

        if(settingValue in self.mapSettings.keys()):
            self.settings[settingName] = self.mapSettings[settingValue]
        else:
            self.settings[settingName] = settingValue
        print("MV settings:", self.settings)

