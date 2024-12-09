"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""

from config.config import Config
import logging
from inference.inference import Inference
from constant.constants import Constants

try:
    from network.yolov5_openvino_object_detection_interface import Yolov5OvObjInterface
except ImportError as e:
    print(f"Failed to import Yolov5OvObjInterface: {e}")

class NetworkInferenceFactory:
    @staticmethod
    def get_network_inference(config):
        log = logging.getLogger('NetworkInferenceFactory')
        network_inference = None

        if not config.engine_name:
            return None

        log.info(f"Hi ,Bahadur i am  Loading Inference Models From Config getEngineName: {config.engine_name.lower()}, DetectionModel: {config.detection_model}")
        engine_name = config.engine_name.lower()

        if engine_name == Constants.YOLO_V5_TRT:
            from network.yolov5_trt_interface import Yolov5Interface
            network_inference = Inference(Yolov5Interface(config.model_path))
        elif engine_name == Constants.ARCFACE_TRT_FV:
            from network.arcface_trt_fv_interface import ArcFaceFvInterface
            network_inference = Inference(ArcFaceFvInterface(config.model_path))
        elif engine_name == Constants.ARCFACE_FRS:
            model=config.model_path.split("--")
            from network.arcface_interface import ArcFaceInterface
            network_inference = Inference(ArcFaceInterface(model[0], model[1]))
        elif engine_name == Constants.YOLO_V5_OV_OBJ:
            network_inference = Inference(Yolov5OvObjInterface(config.model_path, config.width, config.height))
        return network_inference
