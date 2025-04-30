from pygame.time import get_ticks

from draw.rainbow_vendor import RainbowVendor
from model.rectangle import Rectangle
from particle.color_splash_particle import ColorSplashParticle
from particle.particle_emitter import ParticleEmitter

SPLATS_PER_SECOND = 12
LIFESPAN_SECONDS = 1


class ColorSplashEmitter(ParticleEmitter):

    def __init__(self, x: float, y: float, vx: float, vy: float, bounds: Rectangle):
        super().__init__()
        self.step_count = 0
        self.x: float = x
        self.y: float = y
        self.vx = vx
        self.vy = vy
        self.bounds = bounds

        self.start_time = get_ticks()
        self.last_splat_time = None
        self.rainbow_vendor = RainbowVendor(12)

    def update(self, elapsed_millis: int):
        super().update(elapsed_millis)

        total_ticks = get_ticks()

        if total_ticks - self.start_time > LIFESPAN_SECONDS * 1000:
            return

        if self.last_splat_time is None or total_ticks - self.last_splat_time > 1000 / SPLATS_PER_SECOND:
            self.last_splat_time = total_ticks
            self.particles.append(ColorSplashParticle((int(self.x), int(self.y)), 1, self.rainbow_vendor.next_color()))

        self.x += self.vx * elapsed_millis / 1000
        self.y += self.vy * elapsed_millis / 1000

        if self.y > self.bounds.max_y:
            self.vy *= -1
            self.y = self.bounds.max_y
        if self.y < self.bounds.min_y:
            self.vy *= -1
            self.y = self.bounds.min_y
        if self.x > self.bounds.max_x:
            self.vx *= -1
            self.x = self.bounds.max_x
        if self.x < self.bounds.min_x:
            self.vx *= -1
            self.x = self.bounds.min_x

    def is_alive(self) -> bool:
        return self.last_splat_time is None or len(self.particles) > 0