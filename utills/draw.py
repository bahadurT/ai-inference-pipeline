"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
import cv2
import numpy as np
from utills.bounding_box import BoundingBox

class Draw:
    @staticmethod
    def draw_rect(image: np.ndarray, detection_info: BoundingBox) -> np.ndarray:
        """
        Draw a rectangle on the image based on the given detection information.

        Args:
        - image (np.ndarray): Input image.
        - detection_info (BoundingBox): Detection information containing coordinates.

        Returns:
        - np.ndarray: Image with rectangle drawn.
        """
        # Draw rectangle on the image
        cv2.rectangle(image, 
                      (detection_info.left, detection_info.top),
                      (detection_info.left + detection_info.width, detection_info.top + detection_info.height), 
                      (0, 255, 0), 2)

        return image
