import pygame
from pygame import Surface

from draw.led_draw_buffer import LedDrawBuffer
from wled.wled_interface import WledInterface


class PixelPusher:
    def __init__(self, wled_interface: WledInterface):
        self.wled_interface = wled_interface
        self.width = wled_interface.pixel_map.width
        self.height = wled_interface.pixel_map.height
        self.buffer = LedDrawBuffer(self.width, self.height)
        self.expected_pixel_state = Surface((self.width, self.height), pygame.SRCALPHA)

    def send_opaque_pixels(self):
        """Send only non-transparent pixels to WLED."""
        self.wled_interface.send_opaque_pixels(self.buffer.surface)
        self.expected_pixel_state.blit(self.buffer.surface, (0, 0))
        self.buffer = LedDrawBuffer(self.width, self.height)

    def send_all_pixels(self):
        """Send all pixels to WLED, including transparent ones."""
        self.wled_interface.send_all_pixels(self.buffer.surface)
        self.expected_pixel_state = self.buffer.surface.copy()
        self.buffer = LedDrawBuffer(self.width, self.height)