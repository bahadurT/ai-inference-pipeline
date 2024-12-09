"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""

#import yolov5_openvino_object_detector as detector


from yolov5_openvino_object_detector import OpenvinoYolov5

class Yolov5OvObjInterface:
    def __init__(self, model_path: str, width: int, height: int):
        """
        Initialize the Yolov5OvObjInterface with the specified model path, width, and height.

        :param model_path: Path to the YOLOv5 OpenVINO model.
        :param width: Input image width expected by the model.
        :param height: Input image height expected by the model.
        """
        self.detector = OpenvinoYolov5(model_path, width, height)

    def detect(self, image) -> str:
        """
        Perform object detection on the input image.

        :param image: Input image in numpy array format (RGB).
        :return: JSON-formatted string with detection results.
        """
        return self.detector.detect(image, thresh=0.2, batch_size=1)
