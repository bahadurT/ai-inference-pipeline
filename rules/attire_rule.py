"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import io
import gc
import threading
import requests
import time
from datetime import datetime
from datetime import datetime
import math
import logging
from PIL import Image
import numpy as np
import os
import cv2
from shapely.geometry import Polygon
from shapely.geometry import Point

import time
import json
from rules.rule_data import RuleData
from predictions.frs_predictions import FRSPredictions
from predictions.prediction import Prediction
#from faiss_index_builder import FaissIndexBuilder
from pathlib import Path
from boxmot import DeepOCSORT
import math
from collections import OrderedDict
from collections import deque

import supervision as sv
import inspect

from rules.rules import Rules
from rules.rules import CameraRule
from constant.constants import Constants
from rules.arcface_rule import ArcfaceRule
from alerts.event_processor import EventProcessor
import logging


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class AttireRule:
    def __init__(self):
        self.box_annotator = sv.BoxAnnotator()
        self.dim3_box_annotator = sv.Dim3BoxAnnotator()
        self.dim3_color_annotator = sv.Dim3ColorAnnotator()
        
        self.processEvent = EventProcessor()

        self.rule_last_execution = {}

        self.label_annotator = sv.LabelAnnotator()
        self.color_annotator = sv.ColorAnnotator()
        self.circle_anotator = sv.CircleAnnotator()
        self.ellipse_anotator = sv.EllipseAnnotator()

        

        self.arcfacefrs_detections = None
        self.person_detections = None
        self.frame_count = 1
        

        self.log_flag = True
        self.logger = self.setup_logger()
    def setup_logger(self):
        """ Set up the logger. """
        # Check if handlers are already added
        if self.log_flag:
            self.log_flag = False
            self.logger = logging.getLogger('Zone_Intrusion')
            self.logger.setLevel(logging.INFO)

            # Create file handler
            file_handler = logging.FileHandler('TressPass.log')
            file_handler.setLevel(logging.DEBUG)

            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # Create formatter and add it to handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to logger
            #logger.addHandler(file_handler)
            #logger.addHandler(console_handler)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        return self.logger

    
    def process_frame(self, image, camera_id):
        current_time = time.time()
        interval = current_time - self.last_save_time
        if interval >= self.save_interval:
            output_dir = os.path.join('track_output_new', camera_id)
            os.makedirs(output_dir, exist_ok=True)
            file_name = os.path.join(output_dir, f"{camera_id}_{self.track_count:05d}.jpg")
            Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).save(file_name, "JPEG", quality=95)
            #image.save(file_name, "JPEG", quality=95)
            self.track_count += 1
            self.last_save_time = current_time
        image = None  # Free memory after use
    
    
    
    def draw_polygon(self,polygon_points,cv_image):
        # Ensure the list has an even number of elements
        if len(polygon_points) % 2 != 0:
            print("Invalid input: list should contain an even number of elements representing x, y coordinates.")
            return

        points = np.array(polygon_points, np.int32).reshape((-1, 1, 2))
        cv2.polylines(cv_image, [points], isClosed=True, color=(0, 255, 0), thickness=1)  # Green line for the polygon

        # Draw points on the image for clarity
        '''for point in points:
            cv2.circle(cv_image, tuple(point[0]), radius=1, color=(0, 0, 255), thickness=-1)  # Red dots for points'''
        return cv_image
    

    
    def ellipse_to_polygon(self, center, axes, angle, num_points=100):
        """Convert an ellipse to a polygon by sampling points along its perimeter."""
        ellipse_points = []
        theta = np.linspace(0, 2 * np.pi, num_points)
        for t in theta:
            x = center[0] + axes[0] * np.cos(t) * np.cos(angle) - axes[1] * np.sin(t) * np.sin(angle)
            y = center[1] + axes[0] * np.cos(t) * np.sin(angle) + axes[1] * np.sin(t) * np.cos(angle)
            ellipse_points.append((x, y))
        return ellipse_points

    def parse_polygon_points(self, points):
        """Convert a flat list of points into a list of (x, y) tuples."""
        return [(points[i], points[i + 1]) for i in range(0, len(points), 2)]

    def check_ellipse_polygon_intersection(self, center, axes, angle, polygon_points):
        """Check if an ellipse intersects or lies within a polygon."""
        ellipse_polygon = self.ellipse_to_polygon(center, axes, angle)
        ellipse_shapely = Polygon(ellipse_polygon)
        polygon_shapely = Polygon(polygon_points)
        
        return ellipse_shapely.intersects(polygon_shapely) or ellipse_shapely.within(polygon_shapely)
    
    def xywh_to_xyxy(self,xywh: np.ndarray) -> np.ndarray:
        xyxy = xywh.copy()
        xyxy[:, 2] = xywh[:, 0] + xywh[:, 2]  # x_max = x_min + width
        xyxy[:, 3] = xywh[:, 1] + xywh[:, 3]  # y_max = y_min + height
        return xyxy
    
    def clean_predections(self,predictions):
        #self.logger.info(f"Before clean----------------------->{predictions}")
        # for detection in predictions:
        #     self.logger.info(f"{detection}")
        prediction_list = []
        if predictions is not None:
            for detection in predictions:
                label = detection.get_label()
                if label == 'Customer':
                    det = (
                        detection.get_left(),
                        detection.get_top(),
                        detection.get_width(),
                        detection.get_height(),
                        detection.get_score(),
                        detection.get_label()
                    )
                    prediction_list.append(det)
        return prediction_list



    def execute_attire_rules(self, camera, detection_map, category, rule_parameter_list):
        current_time = time.time()

        #image = camera.get_rgb_image()
        #cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Retrieve the RGB image from the camera
        cv_image = camera.get_rgb_image()

        cv_image = cv2.cvtColor(np.array(cv_image), cv2.COLOR_RGB2BGR)
        #self.process_frame(cv_image, camera.getCameraId())
        #cv_image = cv_image.copy()  # Ensure cv_image is writable

        # Ensure that cv_image is not None before processing
        if cv_image is None:
            self.logger.error(f"Failed to get RGB image for camera {camera.getCameraId()}. Skipping frame.")
            return  # Exit the function early if no image is available

        # If valid, copy the frame for further processing
        #frame = cv_image.copy()

        flagSave =0

        data_str = json.dumps(rule_parameter_list)
        camera_rule = RuleData.from_json(data_str)
        lines = camera_rule.get_line_points()
        polygon_points = camera_rule.get_polygon_points()

        current_time = time.time()
        # Ensure the camera has an entry
        if camera.getCameraId() not in self.rule_last_execution:
            self.rule_last_execution[camera.getCameraId()] = {}
        last_execution_time = self.rule_last_execution[camera.getCameraId()].get(category, 0)
        #print("Time left-------------------------------------------------------------------------------------------------------------------------------->",current_time-last_execution_time," ",camera.getCameraId(),"category",category)

        if (Constants.PERSON_DETECTION in detection_map and ((detection_map[Constants.PERSON_DETECTION] and camera_rule.get_active())) and ((current_time-last_execution_time)>camera_rule.get_alert_duration())):
            
            #self.logger.info(f"detection_map: {detection_map}")
            result = detection_map[Constants.PERSON_DETECTION]
            #self.logger.info(f"result: {result}")
            labels_map = camera.get_lables_map()
            #self.logger.info(f"labels_map: {labels_map}")
            labels = labels_map[Constants.PERSON_DETECTION]
            #self.logger.info(f"labels: {labels}")
            prediction_list = Prediction.process_results(result, labels)
            #print(prediction_list,"--------------------------------------------------------------------------------------------------------------------")
            #self.logger.info(f"prediction_list1------------------------------------------------------->: {prediction_list1}")

            

            if camera_rule.get_is_draw_roi():
                cv_image = self.draw_polygon(list(polygon_points[0]), cv_image)
                #cv_image = self.draw_polygon(list(polygon_points[1]), cv_image)
            
            if camera_rule.get_is_draw_line():
                if lines:
                    for line in lines:
                        try:
                            x1, y1, x2, y2 = line
                            cv2.line(cv_image, (x1, y1), (x2, y2), (255, 0, 255), 1)
                        except Exception as e:
                            self.logger.error(f"Error drawing line {line} at line {inspect.currentframe().f_lineno}: {e}")


            if prediction_list is not None:
                
                detection_Lists = []
                #flagSave = 1
                #draw_flag = 1
                counts = 0
                if prediction_list is not None:
                    for detection in prediction_list:
                        label = detection.get_label()
                        if label == 'Person':
                            counts = counts + 1
                            det = [
                                detection.get_left(),
                                detection.get_top(),
                                int(detection.get_left()) + int(detection.get_width()),
                                int(detection.get_top()) + int(detection.get_height()),
                                detection.get_score(),
                                labels.index(label)
                            ]
                            detection_Lists.append(det)
                    #self.logger.info(f"length of detection_Lists: {len(detection_Lists)}")
                    #print(f"length of detection_Lists: {len(detection_Lists)}")
                    if (detection_Lists is not None) and len(detection_Lists)>=1:
                        try:
                            GenAlert = False
                            polyOne = False
                            polyTwo = False
                            server_url = "http://10.0.1.148:8881/analyticImagedEvent"
                            camera_id = "IVISDL01C4"
                            eventType = "Video_Analytic"
                            eventTag = "Zone_Intrusion"
                            sensorName = "Zone_Sensor"
                            sensorId = "IVISDL01C4"
                            serverPort = 0

                            for det in detection_Lists:
                                x1, y1, x2, y2, conf, class_id = det
                                #ellipse = self.create_ellipse(det)
                                #ellipses.append(ellipse)
                                
                                detection_for_annotation = sv.Detections(
                                    xyxy=np.array([[x1, y1, x2, y2]]),
                                    confidence=np.array([1]),  # Assuming confidence is 1 for annotation purposes
                                    class_id=np.array([class_id])  # Including class_id to resolve color
                                )
                                center = ((x1 + x2) // 2, y2)
                                axes = (abs(x2 - x1) // 2, int(0.35 * abs(x2 - x1) // 2))
                                angle = 0

                                if camera_rule.get_isPolygon():
                                    try:
                                        polygon_points1 = self.parse_polygon_points(list(polygon_points[0]))
                                        polyOne = self.check_ellipse_polygon_intersection(center, axes, angle, polygon_points1)
                                        #print("Time left-------------------------------------------------------------------------------------------------------------------------------->",current_time-last_execution_time," ",camera.getCameraId(),"category",category,polyOne)
                                        if polyOne:
                                            GenAlert = True
                                            cv_image = self.box_annotator.annotate(scene=cv_image, detections=detection_for_annotation)
                                            cv_image = self.color_annotator.annotate(scene=cv_image, detections=detection_for_annotation)
                                            cv_image = self.box_corner_annotator.annotate(scene=cv_image, detections=detection_for_annotation)
                                            cv_image = self.ellipse_anotator.annotate(scene=cv_image, detections=detection_for_annotation)

                                            flagSave = 1
                                            
                                    except:
                                        pass
                            if GenAlert:
                                self.logger.info(f"Event Generated:{camera_id},{eventTag},Person : {counts}")
                                #print("Time left-------------------------------------------------------------------------------------------------------------------------------->",current_time-last_execution_time," ",camera.getCameraId(),"category",category," success")
                                self.processEvent.process_event(server_url, cv_image, camera_id, eventType, eventTag, sensorName, sensorId, serverPort, counts, counts)
                                self.rule_last_execution[camera.getCameraId()][category] = current_time
                                GenAlert = False
                                #print("Time left-------------------------------------------------------------------------------------------------------------------------------->",current_time-last_execution_time," ",camera.getCameraId(),"category",category," saving-------------->")
                                
                        except Exception as e:
                            #self.logger.info(f"length of detection_Lists: {len(detection_Lists)}---->{detection_Lists}-----error {e}")
                            self.logger.info(f"length of detection_Lists: {len(detection_Lists)}---->{detection_Lists}-----------------------------------------------------------------------------------------------error {e}")                
                            raise e  
                    else:
                        print(f"No detections for key {Constants.PERSON_DETECTION} : {camera.getCameraId()}")
                else:
                    self.logger.info(f"No detections for key {Constants.PERSON_DETECTION} : {camera.getCameraId()}")
            else:
                print("Tracker Disable: ",prediction_list)
        
        if flagSave:
            self.process_frame(cv_image, camera.getCameraId())
        del cv_image
        cv_image = None  # Dereference to free memory
