"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""

import yolov5_trt_object_detector as detector

class Yolov5Interface:
    def __init__(self, model_path):
        self.detector = detector.TrtYolov5(model_path)

    def detect(self, image) -> str:
        return self.detector.detect(image,0.2,1)
