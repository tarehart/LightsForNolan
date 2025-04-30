from typing import Tuple

from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer


class Particle:
    def __init__(self, pos: Tuple[int, int]):
        self.birth_tick = get_ticks()
        self.x, self.y = pos

    def tick(self):
        pass

    def draw(self, surface: LedDrawBuffer):
        pass

    def is_alive(self) -> bool:
        pass