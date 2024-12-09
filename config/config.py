"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
class Config:
    def __init__(self):
        self.config = ""
        self.weight = None
        self.objData = None
        self.labels = None
        self.detectorType = None
        self.engineName = None  # person, face_recogination
        self.networkName = None  # yolo_v5_trt , "arcface_frs", "arcface_trt_fv"
        self.detectionModel = None
        self.dataconfig = None
        self.noOfClass = 0
        self.width = 0
        self.height = 0
        self.batchSize = 0
        self.isPrimary = True
        self.port = 0
        self.lableFile = ''
        self.width = None
        self.height = None

    def get_lableFile(self) -> str:
        return self.lableFile

    def set_lableFile(self, lableFile: str):
        self.lableFile = lableFile

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def get_batch_size(self):
        return self.batchSize

    def set_batch_size(self, batchSize):
        self.batchSize = batchSize

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_dataconfig(self):
        return self.dataconfig

    def set_dataconfig(self, dataconfig):
        self.dataconfig = dataconfig

    def get_no_of_class(self):
        return self.noOfClass

    def set_no_of_class(self, noOfClass):
        self.noOfClass = noOfClass

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_labels(self):
        return self.labels

    def set_labels(self, labels):
        self.labels = labels

    def get_detector_type(self):
        return self.detectorType

    def set_detector_type(self, detectorType):
        self.detectorType = detectorType

    def get_engine_name(self):
        return self.engineName

    def set_engine_name(self, engineName):
        self.engineName = engineName

    def get_network_name(self):
        return self.networkName

    def set_network_name(self, networkName):
        self.networkName = networkName

    def get_detection_model(self):
        return self.detectionModel

    def set_detection_model(self, detectionModel):
        self.detectionModel = detectionModel

    def get_obj_data(self):
        return self.objData

    def set_obj_data(self, objData):
        self.objData = objData

    def is_primary(self):
        return self.isPrimary

    def set_primary(self, isPrimary):
        self.isPrimary = isPrimary
