import pygame
from pygame.time import Clock, get_ticks

from animation.bouncy_ball_animation import BouncyBallAnimation
from animation.color_fling_animation import ColorFlingAnimation
from animation.interactive_particles_animation import InteractiveParticlesAnimation
from animation.grid_touch_animation import GridTouchAnimation
from diagnostic.host_screen import HostScreen
from diagnostic.logger import Logger
from model.rectangle import Rectangle
from model.serpentine_pixel_map import SerpentinePixelMap
from diagnostic.touch_pane import TouchPane
from wled.pixel_push_mode import PixelPushMode
from wled.pixel_pusher import PixelPusher
from wled.wled_interface import WledInterface

if __name__ == '__main__':

    wled_host = "10.0.0.121"
    udp_port = 21324

    normal_frame_rate = 30
    idle_frame_rate = 1
    idle_after_no_interaction_millis = 60000

    width = 18
    height = 11

    pygame.init()
    interface = WledInterface(wled_host, udp_port, SerpentinePixelMap(width, height))
    pixel_pusher = PixelPusher(interface)
    # animation = BouncyBallAnimation(Rectangle(0, 0, width, height))
    # animation = ColorFlingAnimation(Rectangle(0, 0, width, height))
    # animation = InteractiveParticlesAnimation(Rectangle(0, 0, width, height))
    animation = GridTouchAnimation(Rectangle(0, 0, width, height), cell_width=3, cell_height=3)

    logger = Logger()
    touch_pane = TouchPane()
    host_screen = HostScreen(touch_pane, logger)

    clock = Clock()

    pixel_pusher.buffer.clear_all()
    pixel_pusher.send_all_pixels()

    last_interaction_time = get_ticks()

    while True:

        ticks = get_ticks()
        is_idle_mode = ticks - last_interaction_time > idle_after_no_interaction_millis
        frame_rate = idle_frame_rate if is_idle_mode else normal_frame_rate
        elapsed_millis = clock.tick(frame_rate)

        events = pygame.event.get()
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in events):
            break

        if len(events) > 0:
            last_interaction_time = get_ticks()

        pixel_push_mode = PixelPushMode.SEND_ALL

        if is_idle_mode:
            pixel_pusher.buffer.clear_all()

        else:
            animation.update(elapsed_millis, events, pixel_pusher.buffer)
            pixel_push_mode = animation.draw(pixel_pusher.buffer)
    
            # animation.step(pixel_pusher.buffer)
            touch_pane.step(events)
            host_screen.step(pixel_pusher.expected_pixel_state)

        pixel_pusher.send(pixel_push_mode)

    pygame.quit()
