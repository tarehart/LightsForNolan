import pygame
from pygame.time import Clock

from animation.bouncy_ball_animation import BouncyBallAnimation
from animation.color_fling_animation import ColorFlingAnimation
from diagnostic.host_screen import HostScreen
from diagnostic.logger import Logger
from model.rectangle import Rectangle
from model.serpentine_pixel_map import SerpentinePixelMap
from diagnostic.touch_pane import TouchPane
from wled.pixel_pusher import PixelPusher
from wled.wled_interface import WledInterface

if __name__ == '__main__':

    wled_host = "192.168.0.109"
    udp_port = 21324

    width = 18
    height = 11

    pygame.init()
    interface = WledInterface(wled_host, udp_port, SerpentinePixelMap(width, height))
    pixel_pusher = PixelPusher(interface)
    # animation = BouncyBallAnimation(Rectangle(0, 0, width, height))
    animation = ColorFlingAnimation(Rectangle(0, 0, width, height))

    logger = Logger()
    touch_pane = TouchPane()
    host_screen = HostScreen(touch_pane, logger)

    clock = Clock()

    pixel_pusher.buffer.clear_all()
    pixel_pusher.send_all_pixels()

    while True:
        elapsed_millis = clock.tick(30)
        events = pygame.event.get()
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in events):
            break

        animation.update(elapsed_millis, events, pixel_pusher.buffer)
        animation.draw(pixel_pusher.buffer)

        # animation.step(pixel_pusher.buffer)
        touch_pane.step(events)
        host_screen.step(pixel_pusher.expected_pixel_state)

        pixel_pusher.send_all_pixels()

    pygame.quit()
