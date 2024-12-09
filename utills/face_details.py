"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
from utills.bounding_box import BoundingBox

class FaceDetails:
    def __init__(self, detection: BoundingBox, featureVector: list, name: str, quality: float, gender: str, age: str):
        self._detection = detection
        self._featureVector = featureVector
        self._name = name
        self._quality = quality
        self._gender = gender
        self._age = age

    def get_detection(self) -> BoundingBox:
        return self._detection

    def get_feature_vector(self) -> list:
        return self._featureVector

    def get_name(self) -> str:
        return self._name

    def get_quality(self) -> float:
        return self._quality

    def get_gender(self) -> str:
        return self._gender

    def get_age(self) -> str:
        return self._age

    def __str__(self):
        return (f"FaceDetails(detection={self._detection}, featureVector={self._featureVector}, "
                f"name='{self._name}', quality={self._quality}, gender='{self._gender}', age='{self._age}')")
