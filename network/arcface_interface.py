"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import arcfacefrs_pybind

class ArcFaceInterface:
    def __init__(self, model_face, model_fv):
        self.arcface_frs = arcfacefrs_pybind.ArcFaceFrs(model_face, model_fv)

    def detect(self, image) -> str:
        return self.arcface_frs.detect(image)
