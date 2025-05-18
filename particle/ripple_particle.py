from typing import Tuple
import math
import colorsys
import pygame
from pygame import Surface, Color
from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from particle.particle import Particle

BUFFER_SCALE = 32  # For smooth circle rendering
EXPANSION_SPEED = 15  # Pixels per second
RING_THICKNESS = 2  # Pixels
HUE_ROTATION_SPEED = 0.3  # Full rotations per second

class RippleParticle(Particle):
    def __init__(self, pos: Tuple[float, float], color: Tuple[int, int, int], bounds: Tuple[int, int]):
        super().__init__(pos)
        self.x, self.y = float(pos[0]), float(pos[1])
        self.initial_color = color
        self.bounds = bounds
        self.birth_tick = get_ticks()
        self.radius = 0
        
        # Convert RGB to HSV for easier hue rotation
        rgb_normalized = tuple(c / 255.0 for c in color)
        self.hsv = colorsys.rgb_to_hsv(*rgb_normalized)
        
    def tick(self):
        elapsed_seconds = (get_ticks() - self.birth_tick) / 1000.0
        self.radius = elapsed_seconds * EXPANSION_SPEED

    def draw(self, surface: LedDrawBuffer):
        # Create a larger surface for smooth circle rendering
        big_surface = Surface((surface.width * BUFFER_SCALE, surface.height * BUFFER_SCALE), pygame.SRCALPHA)
        
        # Calculate current color based on hue rotation
        elapsed_seconds = (get_ticks() - self.birth_tick) / 1000.0
        current_hue = (self.hsv[0] + elapsed_seconds * HUE_ROTATION_SPEED) % 1.0
        rgb = colorsys.hsv_to_rgb(current_hue, self.hsv[1], self.hsv[2])
        color = tuple(int(c * 255) for c in rgb)
        
        # Draw outer and inner circles
        center = (
            int(self.x * BUFFER_SCALE),
            int(self.y * BUFFER_SCALE)
        )
        outer_radius = int(self.radius * BUFFER_SCALE)
        inner_radius = int((self.radius - RING_THICKNESS) * BUFFER_SCALE)
        
        if outer_radius > 0:
            pygame.draw.circle(
                big_surface,
                Color(*color, 255),
                center=center,
                radius=outer_radius
            )
            
        if inner_radius > 0:
            pygame.draw.circle(
                big_surface,
                Color(0, 0, 0, 0),  # Transparent
                center=center,
                radius=inner_radius
            )
        
        # Scale down and blend onto the LED surface
        smaller = pygame.transform.smoothscale_by(big_surface, 1 / BUFFER_SCALE)
        surface.draw_image(smaller, 0, 0)

    def is_alive(self) -> bool:
        # Check if the ripple is completely off screen
        max_dimension = max(self.bounds[0], self.bounds[1])
        max_radius = math.sqrt(2) * max_dimension  # Diagonal distance
        return self.radius <= max_radius + RING_THICKNESS 