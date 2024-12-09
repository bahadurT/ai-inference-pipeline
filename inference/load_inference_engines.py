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
from typing import Dict, List
from network.network_inference_factory import NetworkInferenceFactory
from config.config import Config

class LoadInferenceEngines:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.network_inference_map = {}
        self.labels_map = {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def load_labels(self, label_file: str) -> List[str]:
        try:
            with open(label_file, 'r') as file:
                labels = [line.strip() for line in file.readlines()]
                return labels
        except Exception as e:
            self.logger.error(f"Error loading labels: {e}")
            return []

    def load_config(self) -> Dict:
        try:
            with open(self.config_file, 'r') as file:
                self.logger.info(f"Loading configuration from {self.config_file}")
                return json.load(file)
        except FileNotFoundError as e:
            self.logger.error(f"Configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from configuration file: {e}")
            raise

    def init_engines(self) -> None:
        config_data = self.load_config()

        # Process each model entry in the config
        for model_entry in config_data['model']:
            try:
                engine_name = model_entry['engine_name']
                detection_model = model_entry['detection_model']
                model_path = model_entry['model_path']
                image_path = model_entry['image_path']
                label_file = model_entry['lableFile']
                width = model_entry['width']
                height = model_entry['height']

                # Create and configure a Config object
                config = Config()
                config.engine_name = engine_name
                config.detection_model = detection_model
                config.model_path = model_path
                config.image_path = image_path
                config.label_file = label_file
                config.width = width
                config.height = height

                # Get the appropriate network inference instance
                network_inference = NetworkInferenceFactory.get_network_inference(config)
                
                if network_inference is None:
                    self.logger.error(f"No network inference instance created for engine: {engine_name}")
                    continue
                
                # Store the network_inference instance in the map
                self.network_inference_map[detection_model] = network_inference
                
                # Load and store labels in the labels_map
                self.labels_map[detection_model] = self.load_labels(label_file)
                self.logger.info(f"Successfully initialized engine {engine_name} for model {detection_model}")

            except KeyError as e:
                self.logger.error(f"Missing key in configuration for model entry: {e}")
            except Exception as e:
                self.logger.error(f"Error initializing inference engine: {e}")

    def get_network_inference_map(self) -> Dict[str, object]:
        return self.network_inference_map

    def get_labels_map(self) -> Dict[str, List[str]]:
        return self.labels_map
