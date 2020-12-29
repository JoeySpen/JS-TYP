# Vision interface. Defines what a MV technique must implement to work
class VisionInterface:
    def __init__():
        pass

    def getBoxCount(self) -> int:
        pass

    def getFrame(self) -> int:
        pass
    
    # Return all boxes and their positions, useful for hitboxes?
    def getBoxes(self) -> int:
        pass

    def getPeopleCount(self) -> int:
        pass

    def streamVideo(self) -> None:
        pass
