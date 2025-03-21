from draw.led_draw_buffer import LedDrawBuffer
from model.serpentine_pixel_map import SerpentinePixelMap
from .wled_interface import WledInterface
from typing import List, Tuple


class PixelPusher:
    def __init__(self, pixel_map: SerpentinePixelMap, wled_interface: WledInterface):
        self.pixel_map = pixel_map
        self.wled_interface = wled_interface
        self.buffer = LedDrawBuffer(pixel_map)

    def send_opaque_pixels(self):
        """Send only non-transparent pixels to WLED."""
        pixels = self.buffer.get_opaque_pixels()
        self.wled_interface.send_specific_pixels(pixels)
        self.buffer = LedDrawBuffer(self.pixel_map)

    def send_all_pixels(self):
        """Send all pixels to WLED, including transparent ones."""
        pixels = self.buffer.get_all_pixels()
        pixel_array: List[Tuple[int, int, int]] = [(0, 0, 0)] * self.pixel_map.num_pixels

        for pixel in pixels:
            pixel_array[pixel.index] = pixel.color[0:3]

        self.wled_interface.send_all_pixels(pixel_array)
        self.buffer = LedDrawBuffer(self.pixel_map)
