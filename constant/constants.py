"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""

class Constants:
    # Networks Name
    YOLO_V5_TRT = "yolo_v5_trt"
    YOLO_V5_OV_OBJ = "yolo_v5_ov_obj"
    ARCFACE_FRS = "arcface_frs"
    ARCFACE_TRT_FV = "arcface_trt_fv"

    # Rule Constants

    TRESPASS = "trespass"
    FRS = "frs"

    # Engine Names
    PERSON_DETECTION = "person"
    FACE_RECOGINATION = "face_recogination"
    VEHICLE_DETECTION = "vehicle"
    FACE_DETECTION = "face_detection"
    ATTIRE_DETECTION = "attire_detection"
    
    

























    # Repository Types
    REPOSITORY_TYPE_SITESERVER = "SiteServer"
    REPOSITORY_TYPE_SITEMANAGER = "SiteManager"
    REPOSITORY_TYPE_FILE = "File"
    REPOSITORY_TYPE_TEST = "TEST"


    # Stream Request Types
    Stream_Request_Type_VideoServer = "VideoServer"
    Stream_Request_Type_Deepstream = "Deepstream"
    Stream_Request_Type_Deepstream_VideoServer = "Deepstream_VideoServer"
    Stream_Request_Type_Deepstream_Individual = "Deepstream_Individual"
    Stream_Request_Type_Deepstream_Individual_VideoServer = "Deepstream_Individual_VideoServer"
    Stream_Request_Type_Intel = "Intel"

    PACKET_TYPE_VAD_RESULT = 10

    # Encode Types
    ENCODE_TYPE_H264 = 3
    ENCODE_TYPE_JPEG = 0
    ENCODE_TYPE_RGB = 6
    ENCODE_TYPE_GPS = 5

    # Detection Model Names
    YOLO_TRT_DEFAULT = "YOLO_TRT_DEFAULT"
    YOLO_DARKNET_DEFAULT = "YOLO_DARKNET_DEFAULT"
    TLT_SSD_COVERED_FACE = "Tlt_Ssd_Covered_Face"
    TLT_SSD_FIRE_SMOKE = "Tlt_Ssd_Fire_Smoke"
    TLT_SSD_HAND = "Tlt_Ssd_Hand"
    TLT_SSD_HELMET = "Tlt_Ssd_Helmet"
    TLT_SSD_MASK = "Tlt_Ssd_Mask"
    TLT_SSD_PERSON_DETECTION = "tlt_ssd_person_detection"
    TLT_SSD_WEAPON = "Tlt_Ssd_Weapon"
    TLT_SSD_SHUTTER_DEFAULT = "Tlt_Ssd_Shutter_Default"
    TLT_SSD_VAULT_DEFAULT = "Tlt_Ssd_Vault_Default"
    YOLOV5_TRT_SEGMENTATION_MODEL = "yolov5_trt_segmentation_model"
    YOLOV5_OV_FIRE_SEGMENTATION_MODEL = "yolo_v5_openvino_fire_segmentation_model"

    # Pose Estimation Model Names
    OPENVINO_PoseEstimation = "OPENVINO_PoseEstimation"

    # Analytic Types
    Cleanliness = "Cleanliness"
    Premises_Lighting = "Premises Lighting"
    Defective_Camera = "Defective Camera"
    SHUTTER_OPEN_CLOSE_DETECTION = "SHUTTER_OPEN_CLOSE_DETECTION"
    STRONGROOM_OPEN_CLOSE_DETECTION = "STRONGROOM_OPEN_CLOSE_DETECTION"
    TELLERDOOR_OPEN_CLOSE_DETECTION = "TELLERDOOR_OPEN_CLOSE_DETECTION"
    FIRE_SMOKE_DETECTION = "FIRE_SMOKE_DETECTION"
    Affluent_Customer = "Affluent Customer"

    Lift_Waiting_Time = "Lift Waiting Time"
    CROWD_COUNTING = "CROWD_COUNTING"
    Lift_Opening_Closing = "Lift_Opening_Closing"

    # Regions
    REGION_INTERSECT = "Intersect"
    REGION_COMPLETE = "Complete"
    REGION_TOP_LEFT = "Top Left"
    REGION_TOP_CENTER = "Top Center"
    REGION_TOP_RIGHT = "Top Right"
    REGION_CENTER_LEFT = "Center Left"
    REGION_CENTER = "Center"
    REGION_CENTER_RIGHT = "Center Right"
    REGION_BOTTOM_LEFT = "Bottom Left"
    REGION_BOTTOM_CENTER = "Bottom Center"
    REGION_BOTTOM_RIGHT = "Bottom Right"
