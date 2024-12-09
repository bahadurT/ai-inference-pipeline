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

from rules.rule_trespass import RuleTrespass
from rules.attire_rule import AttireRule
from rules.rule_frs import RuleFrs


class RuleExecutor:
    def __init__(self):
        # Initialize any necessary attributes
        self.trespass = {}
        self.trespass_rule_executor = RuleTrespass()
        #self.frs_rule_executor = RuleFrs()

    def execute_rules(self, camera,detection_map):
        try:
            '''for detection_model, detections in detection_map.items():
                print(f"Executing rules for camera {camera.getCameraId()},Detection Model: {detection_model}: {detections}")
                #print(camera.get_rules().get_detection_model_list(),"------------------------models--->")'''

            #print(camera.get_rules().get_rule().get_trespass().get_person().get_confidence(),"--------------------------------->get_confidence()")
            #print(camera.get_model_list(),"----------------->get_model_list()---------------->",camera.getCameraId())

            camera_rule = camera.get_rules()[camera.getCameraId()]
            for rule_name, categories in camera_rule.rule_details.items():
                print(f"  Rule Name: {rule_name} to be Executed -------------------------------------------->",camera.getCameraId())
                if rule_name == Constants.TRESPASS:
                    self.trespass_rule_executor.execute_trespass_rules(camera,detection_map)
                    print(f"  Rule Name: {rule_name} Executed Successfully --------------------------------->",camera.getCameraId())

                elif rule_name == Constants.FRS:
                    #self.frs_rule_executor.execute_frs_rules(camera,detection_map)
                    print(f"  Rule Name: {rule_name} Executed Successfully --------------------------------->",camera.getCameraId())

                '''for category, details_list in categories.items():
                    print(f"    Category: {category}")
                    for details in details_list:
                        for key, value in details.items():
                            print(f"      {key}: {value}")'''
            
        except Exception as e:
            logging.error(f"Error executing rules for camera {camera.getCameraId()}: {e}")
            traceback.print_exc()
