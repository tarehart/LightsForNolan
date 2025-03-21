from typing import Tuple

import pygame

from draw.led_draw_buffer import LedDrawBuffer

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def to_led_coords(proportional_coords: Tuple[float, float], led_dimensions: Tuple[int, int]):
    return (
        int(proportional_coords[0] * led_dimensions[0]),
        int(proportional_coords[1] * led_dimensions[1])
    )


class TouchPane:

    def __init__(self):

        # Initialize Pygame
        pygame.init()

        # Set up fullscreen window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Touch Drawing Test")

        # Store previous touch positions
        self.finger_positions = {}

        self.running = True

    def to_screen_coords(self, proportional_coords: Tuple[float, float]):
        return (
            proportional_coords[0] * self.screen.get_width(),
            proportional_coords[1] * self.screen.get_height()
        )

    def step(self, buffer: LedDrawBuffer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Detect touchscreen movements
            elif event.type == pygame.FINGERMOTION:
                finger_id = event.finger_id  # Track individual fingers


                if finger_id in self.finger_positions:
                    # Draw a line from previous position to current position
                    screen_current = self.to_screen_coords((event.x, event.y))
                    screen_previous = self.to_screen_coords(self.finger_positions[finger_id])
                    pygame.draw.line(self.screen, WHITE, screen_previous, screen_current, 5)

                    led_current = to_led_coords((event.x, event.y), (buffer.width, buffer.height))
                    led_previous = to_led_coords(self.finger_positions[finger_id], (buffer.width, buffer.height))
                    buffer.draw_line(led_previous, led_current, WHITE)


                # Store new position
                self.finger_positions[finger_id] = (event.x, event.y)

            # Remove finger from tracking when lifted
            elif event.type == pygame.FINGERUP:
                if event.finger_id in self.finger_positions:
                    del self.finger_positions[event.finger_id]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_c:  # Press 'C' to clear the screen
                    self.screen.fill(BLACK)

        pygame.display.flip()


