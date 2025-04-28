import math

import pygame
from pygame import Surface, Color
from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from model.rectangle import Rectangle

BUFFER_SCALE = 32

class RisingSunAnimation:
    """
    We can do anti-aliasing more easily than this:
    https://stackoverflow.com/questions/23852917/antialiasing-shapes-in-pygame
    """
    def __init__(self, bounds: Rectangle):
        self.bounds = bounds
        self.width = bounds.width * BUFFER_SCALE
        self.height = bounds.height * BUFFER_SCALE

    def step(self, draw_buffer: LedDrawBuffer):
        total_ticks = get_ticks()
        y = -1 * math.sin(total_ticks * .0002) * self.height * .3 + self.height * 1.3
        big_surface = Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(big_surface, Color(255, 100, 0, 255), center=(self.width / 2, y), radius=self.height * .7)
        smaller = pygame.transform.smoothscale_by(big_surface, 1 / BUFFER_SCALE)
        draw_buffer.draw_image(smaller, 0, 0)
