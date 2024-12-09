"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
import json
import logging
from typing import List

class BoundingBox:
    def __init__(self, left: int, top: int, right: int, bottom: int, width: int, height: int, score: float):
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom
        self._width = width
        self._height = height
        self._score = score

    def get_left(self) -> int:
        return self._left

    def get_top(self) -> int:
        return self._top

    def get_right(self) -> int:
        return self._right

    def get_bottom(self) -> int:
        return self._bottom

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_score(self) -> float:
        return self._score

    def __str__(self):
        return (f"BoundingBox(left={self._left}, top={self._top}, right={self._right}, bottom={self._bottom}, "
                f"width={self._width}, height={self._height}, score={self._score})")

class FaceDetails:
    def __init__(self, detection: BoundingBox, featureVector: List[float], name: str, quality: float, gender: str, age: str):
        self._detection = detection
        self._feature_vector = featureVector
        self._name = name
        self._quality = quality
        self._gender = gender
        self._age = age

    def get_detection(self) -> BoundingBox:
        return self._detection

    def get_feature_vector(self) -> List[float]:
        return self._feature_vector

    def get_name(self) -> str:
        return self._name

    def get_quality(self) -> float:
        return self._quality

    def get_gender(self) -> str:
        return self._gender

    def get_age(self) -> str:
        return self._age

    def __str__(self):
        return (f"FaceDetails(name={self._name}, quality={self._quality}, gender={self._gender}, "
                f"age={self._age}, featureVector={self._feature_vector}, detection={self._detection})")

class FRSPredictions:
    def __init__(self):
        self.results: List[FaceDetails] = []

    def set_results(self, result_str: str):
        try:
            # Clear previous results
            self.results.clear()

            # Clean the result string by removing the extra comma
            result_str = self.clean_result_string(result_str)
            # Parse the result string as JSON and extend the results list
            result_list = json.loads(result_str)
            for result in result_list:
                detection_info = result.get('detection', {})
                feature_vector = result.get('featureVector', [])
                name = result.get('name', "")
                quality = result.get('quality', 0.0)
                gender = result.get('gender', "")
                age = result.get('age', "")
                bounding_box = BoundingBox(
                    left=detection_info.get('left', 0),
                    top=detection_info.get('top', 0),
                    right=detection_info.get('right', 0),
                    bottom=detection_info.get('bottom', 0),
                    width=detection_info.get('width', 0),
                    height=detection_info.get('height', 0),
                    score=detection_info.get('score', 0.0)
                )
                face_details = FaceDetails(
                    detection=bounding_box,
                    featureVector=feature_vector,
                    name=name,
                    quality=quality,
                    gender=gender,
                    age=age
                )
                self.results.append(face_details)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            logging.error(f"Result string: {result_str}")

    @staticmethod
    def clean_result_string(result_str: str) -> str:
        # Remove the extra comma before the closing brackets
        result_str = result_str.replace("},]", "}]")
        return result_str

    def get_results(self) -> List[FaceDetails]:
        return self.results

    def __str__(self) -> str:
        return f"Predictions(results={self.results})"

