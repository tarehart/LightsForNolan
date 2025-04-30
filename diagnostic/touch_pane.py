from typing import Tuple, List

import pygame
from pygame import Surface
from pygame.event import EventType

from draw.led_draw_buffer import LedDrawBuffer

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Set log display parameters
LOG_FONT_SIZE = 20
LOG_HEIGHT = 100  # Reserved space for logs


def to_led_coordinates(proportional_coords: Tuple[float, float], led_dimensions: Tuple[int, int]):
    return (
        int(proportional_coords[0] * led_dimensions[0]),
        int(proportional_coords[1] * led_dimensions[1])
    )


class TouchPane:
    def __init__(self):
        self.diagnostic_surface = Surface((1280, 720))
        self.finger_positions = {}

    def to_diagnostic_coordinates(self, proportional_coords: Tuple[float, float]):
        return (
            proportional_coords[0] * self.diagnostic_surface.get_width(),
            proportional_coords[1] * self.diagnostic_surface.get_height()
        )


    def step(self, events: List[EventType]):
        for event in events:

            # Detect touchscreen movements
            if event.type == pygame.FINGERMOTION:
                finger_id = event.finger_id  # Track individual fingers

                if finger_id in self.finger_positions:
                    # Draw a line from previous position to current position
                    screen_current = self.to_diagnostic_coordinates((event.x, event.y))
                    screen_previous = self.to_diagnostic_coordinates(self.finger_positions[finger_id])
                    pygame.draw.line(self.diagnostic_surface, WHITE, screen_previous, screen_current, 5)

                # Store new position
                self.finger_positions[finger_id] = (event.x, event.y)

            # Remove finger from tracking when lifted
            elif event.type == pygame.FINGERUP:
                if event.finger_id in self.finger_positions:
                    del self.finger_positions[event.finger_id]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.diagnostic_surface.fill(BLACK)


        pygame.display.flip()
