from typing import List

from draw.led_draw_buffer import LedDrawBuffer
from particle.particle import Particle


class ParticleEmitter:

    def __init__(self):
        self.particles: List[Particle] = []

    def update(self, elapsed_millis: int):
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, draw_buffer: LedDrawBuffer):
        for particle in self.particles:
            particle.draw(draw_buffer)

    def is_alive(self) -> bool:
        pass