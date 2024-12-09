"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Oct-2024              *
*                                          *
********************************************
"""
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
