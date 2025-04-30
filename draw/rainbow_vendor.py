from colorsys import hsv_to_rgb
from typing import Tuple


class RainbowVendor:
    def __init__(self, segments: int):
        self.index = 0
        self.segments = segments

    def next_color(self) -> Tuple[int, int, int]:
        hue = (self.index % self.segments) / self.segments
        rgb = hsv_to_rgb(hue, 1, 1)
        self.index += 1
        return int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)