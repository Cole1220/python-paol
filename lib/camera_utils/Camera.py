from dataclasses import dataclass
from typing import List
import cv2

@dataclass
class Camera:
    Index: int
    Capture: cv2.VideoCapture
    Frame: cv2.typing.MatLike

    def __init__(self):
        self.Index = 0
        self.Capture = None
        self.Frames = []
