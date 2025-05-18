from typing import Tuple
import math
import pygame
from pygame import Surface, Color
from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from particle.particle import Particle

BUFFER_SCALE = 32  # For smooth circle rendering

class FloatingParticle(Particle):
    def __init__(self, pos: Tuple[float, float], velocity: Tuple[float, float], color: Tuple[int, int, int], 
                 bounds: Tuple[int, int], spawn_delay: float = 0.0):
        """
        Initialize a floating particle
        :param pos: Initial position
        :param velocity: Initial velocity as (vx, vy)
        :param color: Particle color
        :param bounds: Screen bounds
        :param spawn_delay: Seconds to wait before appearing
        """
        super().__init__(pos)
        self.x, self.y = float(pos[0]), float(pos[1])
        self.vx, self.vy = float(velocity[0]), float(velocity[1])
        self.color = color
        self.bounds = bounds
        self.radius = 1.5  # This will create a ~3 pixel diameter circle
        self.birth_tick = get_ticks()
        self.spawn_delay = spawn_delay
        
    def tick(self):
        elapsed = (get_ticks() - self.birth_tick) / 1000.0
        
        # Don't update during spawn delay
        if elapsed < self.spawn_delay:
            return
            
        # Update position with constant velocity
        self.x += self.vx * 0.016  # Assuming 60fps, so ~16ms per frame
        self.y += self.vy * 0.016
        
        # One-way barriers at screen bounds
        if self.x >= self.bounds[0] - self.radius and self.vx > 0:
            self.vx *= -1
            self.x = self.bounds[0] - self.radius
        if self.x <= self.radius and self.vx < 0:
            self.vx *= -1
            self.x = self.radius
        if self.y >= self.bounds[1] - self.radius and self.vy > 0:
            self.vy *= -1
            self.y = self.bounds[1] - self.radius
        if self.y <= self.radius and self.vy < 0:
            self.vy *= -1
            self.y = self.radius

    def draw(self, surface: LedDrawBuffer):
        elapsed = (get_ticks() - self.birth_tick) / 1000.0
        if elapsed < self.spawn_delay:
            return
            
        # Create a larger surface for smooth circle rendering
        big_surface = Surface((surface.width * BUFFER_SCALE, surface.height * BUFFER_SCALE), pygame.SRCALPHA)
        
        # Draw a circle on the larger surface
        center = (
            int(self.x * BUFFER_SCALE),
            int(self.y * BUFFER_SCALE)
        )
        pygame.draw.circle(
            big_surface, 
            self.color,
            center=center,
            radius=int(self.radius * BUFFER_SCALE)
        )
        
        # Scale down and blend onto the LED surface
        smaller = pygame.transform.smoothscale_by(big_surface, 1 / BUFFER_SCALE)
        surface.draw_image(smaller, 0, 0)

    def is_alive(self) -> bool:
        return True  # Particles float forever unless explicitly removed
        
    def get_position(self) -> Tuple[float, float]:
        return (self.x, self.y) 