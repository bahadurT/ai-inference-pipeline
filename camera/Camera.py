"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
from inference.inference import Inference
from rules.rules import Rules
from rules.rules import CameraRule
class Camera:
    def __init__(self, camera_id, rtsp_url, use_gpu_decoder,network_inference_map,lables_map,camera_rules,detection_model_list,tracker,encode_mode,height,width,formats,fps):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.rules_map={}
        self.use_gpu_decoder = use_gpu_decoder
        self.network_inference_map = network_inference_map
        self.lables_map = lables_map
        self.inference = None
        self.detections = None
        self.rgb_image = None
        self.username = None  # Assuming these are set somewhere else
        self.password = None
        self.drop_frame_interval = None
        self.detection_model = None
        self.camera_rules = camera_rules
        self.detection_model_list = detection_model_list
        self.tracker = tracker
        self.encode_mode = encode_mode
        self.height = height
        self.width = width
        self.formats = formats
        self.fps = fps

        
    def get_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps
        
    def get_formats(self):
        return self.formats

    def set_formats(self, formats):
        self.formats = formats

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def get_encode_mode(self):
        return self.encode_mode

    def set_encode_mode(self, encode_mode):
        self.encode_mode = encode_mode


    def get_tracker(self):
        return self.tracker

    def set_tracker(self, tracker):
        self.tracker = tracker

    def get_model_list(self):
        return self.detection_model_list

    def set_model_list(self, detection_model_list):
        self.detection_model_list = detection_model_list

    def get_rules(self):
        return self.camera_rules

    def set_rules(self, camera_rules):
        self.camera_rules = camera_rules

    def get_lables_map(self):
        return self.lables_map

    def set_lables_map(self, labels_map):
        self.lables_map = lables_map

    def get_detection_model(self):
        return self.detection_model

    def set_detection_model(self, detection_model):
        self.detection_model = detection_model

    def get_inferenceMap(self):
        return self.network_inference_map

    def set_inferenceMap(self, network_inference_map):
        self.network_inference_map = network_inference_map


    def getCameraId(self):
        return self.camera_id

    def getRtspUrl(self):
        return self.rtsp_url

    def isUseGpuDecoder(self):
        return self.use_gpu_decoder

    def get_inference(self):
        return self.inference

    def set_inference(self, inference):
        self.inference = inference

    def get_detections(self):
        return self.detections

    def set_detections(self, detections):
        self.detections = detections

    def get_rgb_image(self):
        return self.rgb_image

    def set_rgb_image(self, image):
        self.rgb_image = image

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getDropFrameInterval(self):
        return self.drop_frame_interval
