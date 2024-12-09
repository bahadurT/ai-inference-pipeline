"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
class InfrenceModel:
    def __init__(self, name, detectionIntervalDelay):
        self.name = name
        self.fps = 1  # Default value
        self.lastProcessingTime = 0  # Default value
        self.dealy = detectionIntervalDelay

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getFps(self):
        return self.fps

    def setFps(self, fps):
        self.fps = fps

    def getLastProcessingTime(self):
        return self.lastProcessingTime

    def setLastProcessingTime(self, lastProcessingTime):
        self.lastProcessingTime = lastProcessingTime

    def getDetectionIntervalDelay(self):
        return self.dealy

    def setDetectionIntervalDelay(self, detectionIntervalDelay):
        self.dealy = detectionIntervalDelay

    def __str__(self):
        return f"InfrenceModel [name={self.name}, fps={self.fps}, lastProcessingTime={self.lastProcessingTime}, detectionIntervalDelay={self.dealy}]"
