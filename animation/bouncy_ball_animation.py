from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from model.rectangle import Rectangle
from draw.rainbow_vendor import RainbowVendor
from datetime import datetime

PIXELS_PER_SEC = 16

class BouncyBallAnimation:
    def __init__(self, bounds: Rectangle):
        self.step_count = 0
        self.x = 0
        self.y = 0
        self.vx = 1
        self.vy = 1

        self.rainbow_vendor = RainbowVendor(20)
        self.ball_size = 3
        self.ball_bounds = Rectangle(
            bounds.x, bounds.y, bounds.width - self.ball_size, bounds.height - self.ball_size
        )  # (x, y, width, height)

    def step(self, draw_buffer: LedDrawBuffer):

        total_ticks = get_ticks()
        new_step_count = int(PIXELS_PER_SEC * total_ticks / 1000)
        if self.step_count == new_step_count:
            return

        self.step_count = new_step_count

        """Move the ball and update the draw buffer."""
        self.x += self.vx
        self.y += self.vy

        if self.y > self.ball_bounds.max_y:
            self.vy *= -1
            self.y = self.ball_bounds.max_y
        if self.y < self.ball_bounds.min_y:
            self.vy *= -1
            self.y = self.ball_bounds.min_y
        if self.x > self.ball_bounds.max_x:
            self.vx *= -1
            self.x = self.ball_bounds.max_x
        if self.x < self.ball_bounds.min_x:
            self.vx *= -1
            self.x = self.ball_bounds.min_x

        if datetime.now().second % 10 > 2:
            draw_buffer.fill_rect(self.x, self.y, 3, 3, self.rainbow_vendor.next_color() + (1,))
        else:
            draw_buffer.fill_rect(self.x, self.y, 5, 5, (0, 0, 0, 255))  # Black
