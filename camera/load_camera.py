"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import json
import logging
from typing import List
from camera.Camera import Camera
from rules.rules import Rules
from rules.rules import CameraRule
class LoadCamera:
    def __init__(self, config_file: str, network_inference_map: dict, lables_map: dict,rules: Rules, detection_model_list,tracker_map: dict):
        self.config_file = config_file
        self.network_inference_map = network_inference_map
        self.lables_map = lables_map
        self.rules_map={}
        self.rules = rules
        self.detection_model_list = detection_model_list
        self.tracker_map = tracker_map
        self.logger = logging.getLogger(self.__class__.__name__)

    def initCamera(self) -> List[Camera]:
        try:
            with open(self.config_file, 'r') as file:
                self.logger.info(f"Loading camera configuration from {self.config_file}")
                data = json.load(file)

                cameras = []
                
                for cam_data in data['cameras']:
                    camera_network_inference_map = {}
                    for detection_model in self.detection_model_list[cam_data['camera_id']]:
                        #print(detection_model,"----------------detection_model---------------------------->,",cam_data['camera_id'])
                        camera_network_inference_map[detection_model] = self.network_inference_map[detection_model]
                    camera = Camera(
                        camera_id=cam_data['camera_id'],
                        rtsp_url=cam_data['rtsp_url'],
                        use_gpu_decoder=cam_data['use_gpu_decoder'],
                        network_inference_map=camera_network_inference_map,  # Pass the inference map to each camera
                        lables_map=self.lables_map,  # Pass the inference map to each camera
                        camera_rules = self.rules,
                        detection_model_list = self.detection_model_list[cam_data['camera_id']],
                        tracker = None,
                        encode_mode=cam_data['encode_mode'],
                        height=cam_data['height'],
                        width=cam_data['width'],
                        formats=cam_data['formats'],
                        fps=cam_data['fps'],
                    )
                    cameras.append(camera)

                return cameras
        except FileNotFoundError as e:
            self.logger.error(f"Camera configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from camera configuration file: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing key in camera configuration: {e}")
            raise


