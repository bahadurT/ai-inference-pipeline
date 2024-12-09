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

class RuleData:
    def __init__(self, confidence=0, bbox_size=None, polygon_points=None, line_points=None, 
                 isLine=False, isPolygon=False, active=False, isBboxSize=False, 
                 tracker=False, server_url='', alert_duration=0, isAlert=False,is_draw_roi=False,is_draw_rect=False,is_save_frame=False,is_draw_lable=False,is_draw_line=False,is_draw_count=False,in_out_points=None,is_draw_circle=False):
        self._confidence = confidence
        self._bbox_size = bbox_size if bbox_size is not None else []
        self._polygon_points = polygon_points if polygon_points is not None else []
        self._line_points = line_points if line_points is not None else []
        self._isLine = isLine
        self._isPolygon = isPolygon
        self._active = active
        self._isBboxSize = isBboxSize
        self._tracker = tracker
        self._server_url = server_url
        self._alert_duration = alert_duration
        self._isAlert = isAlert
        self._is_draw_roi = is_draw_roi
        self._is_draw_rect = is_draw_rect
        self._is_save_frame = is_save_frame
        self._is_draw_lable = is_draw_lable
        self._is_draw_line = is_draw_line
        self._is_draw_count = is_draw_count
        self._in_out_points = in_out_points if in_out_points is not None else []
        self._is_draw_circle = is_draw_circle

    @classmethod
    def from_json(cls, data_str):
        data = json.loads(data_str)
        return cls(
            confidence=data[0]['confidence'],
            bbox_size=data[0]['bbox_size'],
            polygon_points=data[0]['polygon_points'],
            line_points=data[0]['line_points'],
            isLine=data[0]['isLine'],
            isPolygon=data[0]['isPolygon'],
            active=data[0]['active'],
            isBboxSize=data[0]['isBboxSize'],
            tracker=data[0]['tracker'],
            server_url=data[0]['server_url'],
            alert_duration=data[0]['alert_duration'],
            isAlert=data[0]['isAlert'],
            is_draw_roi=data[0]['is_draw_roi'],
            is_draw_rect=data[0]['is_draw_rect'],
            is_save_frame=data[0]['is_save_frame'],
            is_draw_lable=data[0]['is_draw_lable'],
            is_draw_line=data[0]['is_draw_line'],
            is_draw_count=data[0]['is_draw_count'],
            in_out_points=data[0]['in_out_points'],
            is_draw_circle=data[0]['is_draw_circle']
        )

    # Getter methods
    def get_is_draw_circle(self):
        return self._is_draw_circle
        
    def get_in_out_points(self):
        return self._in_out_points
        
    def get_is_draw_count(self):
        return self._is_draw_count

    def get_is_draw_line(self):
        return self._is_draw_line

    def get_is_draw_lable(self):
        return self._is_draw_lable

    def get_is_save_frame(self):
        return self._is_save_frame

    def get_is_draw_rect(self):
        return self._is_draw_rect
    # Getter methods
    def get_is_draw_roi(self):
        return self._is_draw_roi

    # Getter methods
    def get_confidence(self):
        return self._confidence

    def get_bbox_size(self):
        return self._bbox_size

    def get_polygon_points(self):
        return self._polygon_points

    def get_line_points(self):
        return self._line_points

    def get_isLine(self):
        return self._isLine

    def get_isPolygon(self):
        return self._isPolygon

    def get_active(self):
        return self._active

    def get_isBboxSize(self):
        return self._isBboxSize

    def get_tracker(self):
        return self._tracker

    def get_server_url(self):
        return self._server_url

    def get_alert_duration(self):
        return self._alert_duration

    def get_isAlert(self):
        return self._isAlert

'''# The given string
data_str =  [{'confidence': 0.5, 'bbox_size': [250, 600], 'polygon_points': [[0, 23, 12, 39], [0, 23, 12, 39, 25, 45], [0, 23, 12, 39, 25, 45]], 'line_points': [[0, 213, 12, 309], [0, 203, 12, 39], [0, 23, 112, 39], [0, 223, 12, 39]], 'isLine': True, 'isPolygon': True, 'active': True, 'isBboxSize': True, 'tracker': False, 'server_url': '10.0.1.224:8095', 'alert_duration': 300, 'isAlert': False}]
data_str = json.dumps(data_str)

# Create an instance of RuleData from the JSON string
alert_data_instance = RuleData.from_json(data_str)

# Example usage of getter methods
print(alert_data_instance.get_confidence())        # Output: 0.5
print(alert_data_instance.get_bbox_size())         # Output: [250, 600]
print(alert_data_instance.get_polygon_points())    # Output: [[0, 23, 12, 39], [0, 23, 12, 39, 25, 45], [0, 23, 12, 39, 25, 45]]
print(alert_data_instance.get_line_points())       # Output: [[0, 213, 12, 309], [0, 203, 12, 39], [0, 23, 112, 39], [0, 223, 12, 39]]
print(alert_data_instance.get_isLine())            # Output: True
print(alert_data_instance.get_isPolygon())         # Output: True
print(alert_data_instance.get_active())            # Output: True
print(alert_data_instance.get_isBboxSize())        # Output: True
print(alert_data_instance.get_tracker())           # Output: False
print(alert_data_instance.get_server_url())        # Output: 10.0.1.224:8095
print(alert_data_instance.get_alert_duration())    # Output: 300
print(alert_data_instance.get_isAlert())           # Output: False
'''