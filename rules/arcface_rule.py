"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
import logging
from PIL import Image
import numpy as np
import os
import cv2
import time
import json

from rules.rules import Rules
from rules.rules import CameraRule

from constant.constants import Constants
from rules.rule_data import RuleData
from predictions.frs_predictions import FRSPredictions
from predictions.prediction import Prediction
from faissIndexBuilder.faiss_index_builder import FaissIndexBuilder
from pathlib import Path
from boxmot import DeepOCSORT

class ArcfaceRule:
    def __init__(self):
        self.arcfacefrs_detections = None
        self.person_detections = None
        self.frame_count = 1
        self.faiss_builder = FaissIndexBuilder('/home/ivis/analytics/ivis-arcface-frs/face_db_fv/')
        self.faiss_builder.load_feature_vectors()
        self.index = None
        self.matched_face = {}
        self.tracker_class = {'camera1': 1, 'camera2': 2}
        self.track_count = 1
        self.save_interval = 0.100
        self.tracker = None
        self.last_save_time = time.time()
        self.tracker_reset_interval = 3600  # 1 hour
        self.last_tracker_reset_time = time.time()
        self.saved_tracker_ids = {}
        self.tracker_ID = 0
        self.current_tracker_ID = 0
        self.create_tracker_flag = 1
        self.tracker_map = {}

        self.logger = logging.getLogger('ArcfaceRule')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('frslog.log')
        file_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    #@profile
    def get_tracker(self, camera):
        camera_id = camera.getCameraId()
        self.logger.info(f"Creating new tracker for {camera_id}")
        self.tracker_map[camera_id] = DeepOCSORT(model_weights=Path("mobilenetv2_x1_0_market1501.pt"), device='cuda:0', fp16='False',max_objs=500,max_age=50)
        #self.tracker_map[camera_id] = cv2.TrackerKCF_create()

    
    def process_frame(self, cv_image, camera_id):
        current_time = time.time()
        interval = current_time - self.last_save_time
        if interval >= self.save_interval:
            output_dir = os.path.join('track_output_new', camera_id)
            os.makedirs(output_dir, exist_ok=True)
            file_name = os.path.join(output_dir, f"{camera_id}_{self.track_count:05d}.jpg")
            Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)).save(file_name, "JPEG", quality=95)
            self.track_count += 1
            self.last_save_time = current_time
        cv_image = None  # Free memory after use

    #@profile
    def search_similar_vectors(self, query_feature, k=5):
        try:
            if query_feature.ndim == 1:
                query_feature = np.expand_dims(query_feature, axis=0)
            elif query_feature.ndim == 2 and query_feature.shape[0] == 1:
                query_feature = np.squeeze(query_feature, axis=0)
            else:
                raise ValueError(f"Unexpected shape for query feature: {query_feature.shape}")

            if self.index is None:
                self.index = self.faiss_builder.create_faiss_index(query_feature.shape[1])

            t1 = time.time()
            self.matched_face = {}
            Distance, I = self.index.search(query_feature, k=k)
            t2 = time.time()
            time_taken = (t2 - t1)

            for i in range(len(I[0])):
                name_ = self.faiss_builder.names[I[0][i]]
                distance_ = Distance[0][i]
                self.matched_face[name_] = float(distance_)
            del Distance
            del I

        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error reading query feature: {e}")
    #@profile
    def reset_tracker(self, camera):
        camera_id = camera.getCameraId()
        #self.saved_tracker_ids[camera_id] = self.track_count
        self.logger.info(f"Resetting tracker for {camera_id}, track count: {self.track_count}")
        del self.tracker_map[camera_id]
        self.get_tracker(camera)
        self.track_count = self.saved_tracker_ids[camera_id]
        self.last_tracker_reset_time = time.time()
    #@profile
    def execute_arcface_rules(self, camera, detection_map, category, rule_parameter_list):
        try:
            current_time = time.time()
            cv_image = camera.get_rgb_image()

            #self.logger.info(f"Available keys in detection_map: {detection_map.keys()}")

            if Constants.PERSON_DETECTION in detection_map and detection_map[Constants.PERSON_DETECTION]:
                result = detection_map[Constants.PERSON_DETECTION]
                labels_map = camera.get_lables_map()
                labels = labels_map[Constants.PERSON_DETECTION]
                prediction_list = Prediction.process_results(result, labels)

                self.logger.info(f"prediction_list: {prediction_list}")

                camera_rule = camera.get_rules()[camera.getCameraId()]
                data_str = json.dumps(rule_parameter_list)
                camera_rule = RuleData.from_json(data_str)

                if camera_rule.get_tracker():
                    if self.create_tracker_flag == 1:
                        self.create_tracker_flag = 0
                        self.get_tracker(camera)
                    flag = 0
                    detection_Lists = []
                    if prediction_list:
                        for detection in prediction_list:
                            det = [detection.get_left(), detection.get_top(), detection.get_left() + detection.get_width(), detection.get_top() + detection.get_height(), detection.get_score(), self.tracker_class[camera.getCameraId()]]
                            detection_Lists.append(det)
                        
                        dets = np.array(detection_Lists)
                        detection_Lists.clear()  # Clear the list after conversion
                        
                        if dets.size > 0:
                            updated_dets = self.tracker_map[camera.getCameraId()].update(dets, cv_image)
                            updated_dets = updated_dets.astype(int)
                            for det in updated_dets:
                                flag = 1
                                x1, y1, x2, y2, track_id, _, _, _ = det
                                self.current_tracker_ID = track_id
                                self.logger.info(f"{camera.getCameraId()} Current Tracker ID: {track_id}:Updated:  {self.tracker_ID + self.current_tracker_ID}")
                        else:
                            updated_dets = self.tracker_map[camera.getCameraId()].update(np.empty((0, 6)), cv_image)
                        
                        if (current_time - self.last_tracker_reset_time >= self.tracker_reset_interval) and flag == 0:
                            self.tracker_ID = self.tracker_ID + self.current_tracker_ID
                            self.reset_tracker(camera)
                else:
                    pass
                    #self.logger.info(f"No detections for key {Constants.PERSON_DETECTION} : {camera.getCameraId()}")
                    #updated_dets = self.tracker_map[camera.getCameraId()].update(np.empty((0, 6)), cv_image)

            if Constants.FACE_RECOGINATION in detection_map:
                raw_detections = detection_map[Constants.FACE_RECOGINATION]
                self.logger.info(f"raw_detections: {raw_detections}")
                if raw_detections:
                    predictions = FRSPredictions()
                    predictions.set_results(raw_detections)
                    face_details_list = predictions.get_results()

                    if face_details_list:
                        for face_detail in face_details_list:
                            detection = face_detail.get_detection()
                            feature_vector = face_detail.get_feature_vector()
                            cv2.rectangle(cv_image, (detection.get_left(), detection.get_top()), 
                                          (detection.get_left() + detection.get_width(), detection.get_top() + detection.get_height()), 
                                          (0, 255, 0), 2)
                            self.matched_face = {}
                            query_feature = np.array(feature_vector, dtype=np.float32)
                            query_feature = query_feature / np.linalg.norm(query_feature) if np.linalg.norm(query_feature) > 0 else query_feature
                            self.search_similar_vectors(query_feature, 5)
                            '''for name, distance in self.matched_face.items():
                                if distance > 0.45:
                                    text = name.split(":")[0] + ": " + str(distance)
                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    font_scale = 0.5
                                    color = (0, 255, 0)
                                    thickness = 1
                                    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                                    text_x = detection.get_left()
                                    text_y = detection.get_top() - 10
                                    if text_y < 0:
                                        text_y = detection.get_top() + text_size[1] + 10
                                    cv2.putText(cv_image, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

                                    output_dir = os.path.join('output', camera.getCameraId())
                                    os.makedirs(output_dir, exist_ok=True)
                                    file_name = os.path.join(output_dir, f"{name}_{camera.getCameraId()}_{self.frame_count:05d}.jpg")
                                    Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)).save(file_name, "JPEG", quality=95)
                                    self.frame_count += 1'''

            if Constants.FACE_DETECTION in detection_map:
                face_detections = detection_map[Constants.FACE_DETECTION]
                print(face_detections,"--------------------------------------------->face_detections")
                self.logger.info(f"face_detections: {face_detections}")
                #self.logger.error(f"face_detections: {face_detections}")

            if Constants.ARCFACE_TRT_FV in detection_map:
                fv_detections = detection_map[Constants.ARCFACE_TRT_FV]
                print("fv_detections: ",len(str(fv_detections)))
                self.logger.info(f"fv_detections: {len(str(fv_detections))}")
                #self.logger.error(f"face_detections: {fv_detections}")
            else:
                self.logger.warning(f"No relevant detection key found in detection_map for {camera.getCameraId()}")

        except Exception as e:
            self.logger.error(f"Error in execute_arcface_rules: {e}")

        cv_image = None  # Dereference to free memory

    