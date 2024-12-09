"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import os
import cv2
import time
import logging
import traceback
from predictions.frs_predictions import FRSPredictions
from predictions.prediction import Prediction
from utills.draw import Draw
import json
from constant.constants import Constants
class Inference:
    def __init__(self, inference_pointer):
        self.inference_pointer = inference_pointer
        self.labels = []
        print("----------------------- init Detection -------------------------")

    def process_image(self, image: str, detection_model: str, camera):
        camera.set_detection_model(detection_model)
        try:
            if image is None:
                logging.error(f"Failed to load image: {image}")
                return None
            #t1 = time.time()
            #result = self.inference_pointer.detect(image)
            camera.set_detections(self.inference_pointer.detect(image))
            #t2 = time.time()
            # print(f"Time taken: --------{camera.getCameraId()}--------------------------------------> {(t2 - t1):.4f} ms")
        except Exception as e:
            print("-------------------------------------------Exception--------",e)
            logging.error(f"Error processing image:  {e}")
            traceback.print_exc()

