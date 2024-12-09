"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import arcfacefv as detector
class ArcFaceFvInterface:
    def __init__(self, model_path):
        self.detector = detector.ArcFaceFv(model_path)

    def detect(self, image) -> str:
        return self.detector.detect(image)
