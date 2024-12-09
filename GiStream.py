"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""

import sys
print("Python Path:", sys.path)
import sys
import argparse
import logging
from inference.load_inference_engines import LoadInferenceEngines
from camera.load_camera import LoadCamera
from pipeline.start_pipeline import StartPipeline
from rules.rules import Rules, CameraRule

import cv2
import numpy as np


class GiStream:
    def __init__(self, config_file: str, inference_config_file: str, rules_config: str):
        self.config_file = config_file
        self.rules_config = rules_config
        self.inference_config_file = inference_config_file
        self.cameras = []
        self.network_inference_map = {}
        self.labels_map = {}
        self.rules_map = {}
        self.rules = None
        self.detection_model_list = {}
        
        self.tracker_map = {}  # Initialize tracker map
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    def load_inference_engines(self):
        self.logger.info("Loading inference engines...")
        inference_loader = LoadInferenceEngines(self.inference_config_file)
        inference_loader.init_engines()
        self.network_inference_map = inference_loader.get_network_inference_map()
        self.labels_map = inference_loader.get_labels_map()
        print("------------->", self.labels_map)
        self.logger.info("Inference engines loaded successfully.")

    def load_rules(self):
        import json
        self.logger.info("Loading rules...")
        with open(self.rules_config, 'r') as f:
            data = json.load(f)
        
        rules = {}
        for camera_id, camera_data in data.items():
            for config in camera_data:
                self.detection_model_list[camera_id] = config.get("detection_model_list", [])
                
                rule_list = config.get("rule_list", [])
                camera_rule = CameraRule(rule_list)
                rules[camera_id] = camera_rule
        print(self.detection_model_list)
        self.rules = rules
        self.logger.info("Rules loaded successfully.")
        
    def load_cameras(self):
        self.logger.info("Loading cameras...")

        self.tracker_map['camera1'] = None
        self.tracker_map['camera2'] = None

        camera_loader = LoadCamera(self.config_file, self.network_inference_map, self.labels_map, self.rules, self.detection_model_list, self.tracker_map)
        self.cameras = camera_loader.initCamera()
        if not self.cameras:
            self.logger.error("No cameras configured.")

    def start_pipeline(self):
        if not self.cameras:
            self.logger.error("No cameras to start pipeline.")
            return

        self.logger.info("Starting pipeline...")
        pipeline = StartPipeline(self.cameras)
        pipeline.run()

    def run(self):
        try:
            self.load_inference_engines()
            self.load_rules()
            self.load_cameras()
            self.start_pipeline()
        except Exception as e:
            self.logger.error(f"Failed to run GiStream: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="GiStream Video Analytics Pipeline")
    parser.add_argument('--config', type=str, required=True, help="Path to the camera configuration file")
    parser.add_argument('--inference', type=str, required=True, help="Path to the inference configuration file")
    parser.add_argument('--rules', type=str, required=True, help="Path to the rules configuration file")

    args = parser.parse_args()

    gi_stream = GiStream(config_file=args.config, inference_config_file=args.inference, rules_config=args.rules)
    gi_stream.run()


if __name__ == "__main__":
    main()
