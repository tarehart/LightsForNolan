from typing import Tuple
from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from particle.particle import Particle

class StaticFadeParticle(Particle):
    LIFESPAN_MILLIS = 1000  # Fade over 1 second
    
    def __init__(self, pos: Tuple[float, float], color: Tuple[int, int, int]):
        super().__init__(pos)
        self.x, self.y = float(pos[0]), float(pos[1])
        self.color = color
        self.radius = 1
        self.birth_tick = get_ticks()

    def tick(self):
        pass

    def draw(self, surface: LedDrawBuffer):
        age = get_ticks() - self.birth_tick
        alpha = 1.0 - (age / self.LIFESPAN_MILLIS)
        if alpha <= 0:
            return
            
        faded_color = (
            int(self.color[0] * alpha),
            int(self.color[1] * alpha),
            int(self.color[2] * alpha)
        )
        
        surface.fill_rect(int(self.x - self.radius), int(self.y - self.radius),
                         self.radius * 2, self.radius * 2, faded_color)

    def is_alive(self) -> bool:
        return get_ticks() - self.birth_tick < self.LIFESPAN_MILLIS 