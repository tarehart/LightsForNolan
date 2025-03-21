from pygame.time import Clock

from animation.bouncy_ball_animation import BouncyBallAnimation
from model.rectangle import Rectangle
from model.serpentine_pixel_map import SerpentinePixelMap
from touch.touch_pane import TouchPane
from wled.pixel_pusher import PixelPusher
from wled.wled_interface import WledInterface

if __name__ == '__main__':

    wled_host = "192.168.0.109"
    udp_port = 21324

    width = 18
    height = 11

    interface = WledInterface(wled_host, udp_port)
    pixel_pusher = PixelPusher(SerpentinePixelMap(width, height), interface)
    animation = BouncyBallAnimation(Rectangle(0, 0, width, height))

    touch_pane = TouchPane()

    clock = Clock()

    pixel_pusher.buffer.clear_all()
    pixel_pusher.send_all_pixels()


    while True:
        clock.tick(30)
        touch_pane.step(pixel_pusher.buffer)
        animation.step(pixel_pusher.buffer)
        pixel_pusher.send_opaque_pixels()


