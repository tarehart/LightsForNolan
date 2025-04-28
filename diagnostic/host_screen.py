import pygame
from pygame import Surface

from diagnostic.logger import Logger
from diagnostic.touch_pane import TouchPane

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Set log display parameters
LOG_FONT_SIZE = 20
LOG_HEIGHT = 600  # Reserved space for logs


class HostScreen:
    def __init__(self, touch_pane: TouchPane, logger: Logger):

        # Set up fullscreen window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Touch Drawing Test")

        self.font = pygame.font.SysFont(None, LOG_FONT_SIZE)

        # Log messages storage
        self.logger = logger
        self.max_logs = LOG_HEIGHT // LOG_FONT_SIZE

        self.touch_pane = touch_pane


    def render_led_buffer(self, surface: Surface):
        led_scaled = pygame.transform.scale_by(surface,16)
        self.screen.fill((0, 0, 0, 255), (0, 0, led_scaled.get_width(), led_scaled.get_height()))
        self.screen.blit(led_scaled, (0, 0))

    def render_logs(self):
        log_area = Surface((400, LOG_HEIGHT), pygame.SRCALPHA)
        log_area.fill(GRAY)

        for i, log in enumerate(self.logger.logs[-self.max_logs:]):
            text_surface = self.font.render(log, True, WHITE)
            log_area.blit(text_surface, (10, i * LOG_FONT_SIZE))

        self.screen.blit(log_area, (0, 16 * 11))

    def step(self, expected_grid_state: Surface):

        self.render_led_buffer(expected_grid_state)
        self.render_logs()
        self.screen.blit(self.touch_pane.diagnostic_surface, (450, 0))
        pygame.display.flip()
