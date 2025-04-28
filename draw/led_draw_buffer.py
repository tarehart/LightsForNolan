from typing import Tuple

import pygame
from pygame import Surface


class LedDrawBuffer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # Create an image with an RGBA mode
        self.surface = Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int]):
        pygame.draw.line(self.surface, color, start, end)

    def fill_rect(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int, int]):
        pygame.draw.rect(self.surface, color, (x, y, width, height))

    def draw_image(self, image: Surface, x: int, y: int):
        self.surface.blit(image, (x, y))

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int, int], size: int):
        font = pygame.font.SysFont("Arial", size)
        text_image = font.render(text, antialias=False, color=color)
        self.draw_image(text_image, x, y)

    def clear_all(self, color: Tuple[int, int, int, int] = (0, 0, 0, 255)):
        """Clear the entire buffer with a given color."""
        self.fill_rect(0, 0, self.width, self.height, color)
