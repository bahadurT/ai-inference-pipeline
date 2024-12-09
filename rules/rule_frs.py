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

import time
import logging
import traceback
from rules.rules import Rules
from rules.rules import CameraRule
from constant.constants import Constants
from rules.arcface_rule import ArcfaceRule

class RuleFrs:
    def __init__(self):
        # Initialize any necessary attributes
        self.frs = {}
        self.arcfacefrs_rule_executor = ArcfaceRule()

    def execute_frs_rules(self, camera,detection_map):
        try:
            '''for detection_model, detections in detection_map.items():
                print(f"Executing rules for camera {camera.getCameraId()},Detection Model: {detection_model}: {detections}")'''
            camera_rule = camera.get_rules()[camera.getCameraId()]
            for rule_name, categories in camera_rule.rule_details.items():

                #print(f"  Rule Name: {rule_name}")
                for category, details_list in categories.items():
                    print(f"    Category: {category}-----------------to be executed------------------->",camera.getCameraId())
                    if category == Constants.PERSON_DETECTION:
                        print(f"    Category: {category}------------ executed sucessfully ------------>",camera.getCameraId())
                    elif category == Constants.FACE_RECOGINATION:
                        print(f"    Category: {category}-----------------to be executed--------------------------------------------------------------------------------calling->",camera.getCameraId())
                        self.arcfacefrs_rule_executor.execute_arcface_rules(camera,detection_map,category, details_list)
                        print(f"    Category: {category}------------ executed sucessfully ------------>",camera.getCameraId())
                    elif category == Constants.VEHICLE_DETECTION:
                        print(f"    Category: {category}------------ executed sucessfully ------------>",camera.getCameraId())
                    '''for details in details_list:
                        for key, value in details.items():
                            print(f"      {key}: {value}")'''

        except Exception as e:
            logging.error(f"Error executing rules for camera {camera.getCameraId()}: {e}")
            traceback.print_exc()