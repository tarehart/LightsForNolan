from typing import List, Tuple, Dict
import random
import math
import pygame
from pygame.event import EventType

from animation.bouncy_ball_animation import BouncyBallAnimation
from draw.led_draw_buffer import LedDrawBuffer
from draw.rainbow_vendor import RainbowVendor
from input.drag_chunker import DragChunker
from model.rectangle import Rectangle
from particle.floating_particle import FloatingParticle
from particle.ripple_particle import RippleParticle
from wled.pixel_push_mode import PixelPushMode


def to_led_coordinates(proportional_coords: Tuple[float, float], led_dimensions: Tuple[int, int]) -> Tuple[float, float]:
    return (
        proportional_coords[0] * led_dimensions[0],
        proportional_coords[1] * led_dimensions[1]
    )

PARTICLE_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
]

MIN_SPEED = 2
MAX_SPEED = 8
SPAWN_MARGIN = 3  # How far outside the bounds to spawn particles
TARGET_MARGIN = 1  # How far within the bounds the target must be

class InteractiveParticlesAnimation:
    def __init__(self, bounds: Rectangle):
        self.bounds = bounds
        self.drag_chunkers: Dict[str, DragChunker] = {}
        self.particles: List[FloatingParticle] = []
        self.ripples: List[RippleParticle] = []
        info = pygame.display.Info()
        self.screen_dimensions = (info.current_w, info.current_h)
        self.rainbow_vendor = RainbowVendor(6)
        
        # Load sound effect
        self.droplet_sound = pygame.mixer.Sound("sounds/droplet.wav")
        self.droplet_sound.set_volume(1.0)  # Set to maximum volume

        self.number_sounds = [
            pygame.mixer.Sound(f'sounds/{i + 1}.wav')
            for i in range(10)
        ]
        for number_sound in self.number_sounds:
            number_sound.set_volume(1.0)

        self.celebration_sound = pygame.mixer.Sound('sounds/ode_to_joy.mp3')
        self.celebration_sound.set_volume(0.7)


        self.number_index = 0
        self.celebration_animation: BouncyBallAnimation | None = None
        self.celebration_start_ticks = pygame.time.get_ticks()

        # Create initial particles
        for _ in range(4):
            self.spawn_new_particle()
        
    def spawn_new_particle(self):
        # All particles spawn from the bottom
        spawn_pos = (self.bounds.width / 2, self.bounds.height + SPAWN_MARGIN)
        
        # Choose random target within bounds to aim at
        target_x = random.uniform(TARGET_MARGIN, self.bounds.width - TARGET_MARGIN)
        target_y = random.uniform(TARGET_MARGIN, self.bounds.height - TARGET_MARGIN)
        
        # Calculate velocity vector aimed at target
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        dx = target_x - spawn_pos[0]
        dy = target_y - spawn_pos[1]
        dist = math.sqrt(dx * dx + dy * dy)
        velocity = ((dx / dist) * speed, (dy / dist) * speed)
        
        # Create particle with next color from the rainbow vendor
        color = self.rainbow_vendor.next_color()

        particle = FloatingParticle(
            spawn_pos,
            velocity,
            color,
            (self.bounds.width, self.bounds.height)
        )
        self.particles.append(particle)

    def check_collision(self, point: Tuple[float, float], particle_pos: Tuple[float, float], radius: float) -> bool:
        dx = point[0] - particle_pos[0]
        dy = point[1] - particle_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < radius

    def handle_interaction(self, pos_normalized: Tuple[float, float], led_dimensions: Tuple[int, int]):
        """Handle an interaction at the given normalized position"""
        led_pos = to_led_coordinates(pos_normalized, led_dimensions)
        
        # Check for collisions with floating particles
        for particle in list(self.particles):  # Create a copy of the list to safely modify
            if self.check_collision(led_pos, particle.get_position(), particle.radius):
                # Create ripple effect at the particle's position
                ripple = RippleParticle(
                    particle.get_position(),
                    particle.color,
                    (self.bounds.width, self.bounds.height)
                )
                self.ripples.append(ripple)
                self.droplet_sound.play()  # Play sound when ripple is created

                number_sound = self.number_sounds[self.number_index]
                number_sound.play()
                self.number_index = (self.number_index + 1) % 10

                if self.number_index == 0:
                    # We reached the end and looped around, let's celebrate
                    # How can we change the blend mode
                    self.celebration_animation = BouncyBallAnimation(self.bounds)
                    self.celebration_start_ticks = pygame.time.get_ticks()
                    self.celebration_sound.play()
                
                # Remove the particle and spawn a replacement
                self.particles.remove(particle)
                self.spawn_new_particle()
                break  # Only handle one collision per interaction

    def update(self, elapsed_millis: int, events: List[EventType], draw_buffer: LedDrawBuffer):

        if self.celebration_animation is not None:
            self.celebration_animation.update()
            if pygame.time.get_ticks() - self.celebration_start_ticks > 27000:
                self.celebration_animation = None
            return

        # Handle events
        for event in events:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                # Get position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = (event.pos[0] / self.screen_dimensions[0], event.pos[1] / self.screen_dimensions[1])
                    # Set up drag tracker for mouse
                    self.drag_chunkers["mouse"] = DragChunker(
                        pos,
                        200
                    )
                else:  # FINGERDOWN
                    pos = (event.x, event.y)
                    # Set up drag tracker for finger
                    self.drag_chunkers[event.finger_id] = DragChunker(pos, 200)

                self.handle_interaction(pos, (draw_buffer.width, draw_buffer.height))

            elif event.type == pygame.MOUSEBUTTONUP and "mouse" in self.drag_chunkers:
                del self.drag_chunkers["mouse"]

            elif event.type == pygame.FINGERUP:
                pointer_id = event.finger_id
                if pointer_id in self.drag_chunkers:
                    del self.drag_chunkers[pointer_id]

            elif event.type == pygame.FINGERMOTION or event.type == pygame.MOUSEMOTION:
                pointer_id = None
                position_normalized = None
                if event.type == pygame.FINGERMOTION:
                    pointer_id = event.finger_id
                    position_normalized = (event.x, event.y)
                elif event.type == pygame.MOUSEMOTION:
                    pointer_id = "mouse"
                    position_normalized = (
                        event.pos[0] / self.screen_dimensions[0], 
                        event.pos[1] / self.screen_dimensions[1]
                    )

                if pointer_id is not None and position_normalized is not None:
                    if pointer_id in self.drag_chunkers:
                        chunker = self.drag_chunkers[pointer_id]
                        chunker.update(position_normalized, elapsed_millis)
                        
                        if chunker.is_chunk_ready():
                            chunk = chunker.get_chunk_and_reset()
                            led_dimensions = (draw_buffer.width, draw_buffer.height)
                            self.handle_interaction(chunk.end, led_dimensions)

                    elif event.type == pygame.FINGERMOTION:
                        self.drag_chunkers[pointer_id] = DragChunker(position_normalized, 200)

        # Update particles
        for particle in self.particles:
            particle.tick()

        # Update and clean up ripples
        self.ripples = [r for r in self.ripples if r.is_alive()]
        for ripple in self.ripples:
            ripple.tick()

    def draw(self, draw_buffer: LedDrawBuffer) -> PixelPushMode:

        if self.celebration_animation is not None:
            return self.celebration_animation.draw(draw_buffer)

        # Draw all particles
        for particle in self.particles:
            particle.draw(draw_buffer)
            
        # Draw ripple effects
        for ripple in self.ripples:
            ripple.draw(draw_buffer)

        return PixelPushMode.SEND_ALL