from typing import Tuple

from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from draw.rainbow_vendor import RainbowVendor
from particle.particle import Particle


LIFESPAN_MILLIS = 3000

class ColorSplashParticle(Particle):

    def __init__(self, pos: Tuple[int, int], radius: int, color: Tuple[int, int, int]):
        super().__init__(pos)
        self.radius = radius
        self.color = color
        self.rainbow_vendor = RainbowVendor(20)

    def tick(self):
        pass

    def draw(self, surface: LedDrawBuffer):
        surface.fill_rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2, self.color)

    def is_alive(self) -> bool:
        return get_ticks() - self.birth_tick < LIFESPAN_MILLIS