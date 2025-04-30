from typing import List, Tuple, Dict

import pygame
from pygame.event import EventType

from draw.led_draw_buffer import LedDrawBuffer
from input.drag_chunker import DragChunker
from model.rectangle import Rectangle
from particle.color_splash_emitter import ColorSplashEmitter


def to_led_coordinates(proportional_coords: Tuple[float, float], led_dimensions: Tuple[int, int]) -> Tuple[float, float]:
    return (
        proportional_coords[0] * led_dimensions[0],
        proportional_coords[1] * led_dimensions[1]
    )


SPEED_MULTIPLIER = 4


class ColorFlingAnimation:
    def __init__(self, bounds: Rectangle):
        self.bounds = bounds
        self.drag_chunkers: Dict[str, DragChunker] = {}
        self.emitters: List[ColorSplashEmitter] = []
        info = pygame.display.Info()
        self.screen_dimensions = (info.current_w, info.current_h)

    def update(self, elapsed_millis: int, events: List[EventType], draw_buffer: LedDrawBuffer):

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drag_chunkers["mouse"] = DragChunker(
                    (event.pos[0] / self.screen_dimensions[0], event.pos[1] / self.screen_dimensions[1]), 200)

            elif event.type == pygame.MOUSEBUTTONUP:
                del self.drag_chunkers["mouse"]

            elif event.type == pygame.FINGERUP:
                pointer_id = event.finger_id
                if pointer_id in self.drag_chunkers:
                    del self.drag_chunkers[pointer_id]

            elif event.type == pygame.FINGERMOTION or event.type == pygame.MOUSEMOTION:
                # Detect touchscreen movements
                pointer_id = None
                position_normalized = None
                if event.type == pygame.FINGERMOTION:
                    pointer_id = event.finger_id  # Track individual fingers
                    position_normalized = (event.x, event.y)
                elif event.type == pygame.MOUSEMOTION:
                    pointer_id = "mouse"
                    position_normalized = (
                    event.pos[0] / self.screen_dimensions[0], event.pos[1] / self.screen_dimensions[1])


                if pointer_id is not None and position_normalized is not None:

                    if pointer_id in self.drag_chunkers:

                        chunker = self.drag_chunkers[pointer_id]
                        chunker.update(position_normalized, elapsed_millis)
                        if chunker.is_chunk_ready():
                            chunk = chunker.get_chunk_and_reset()
                            led_dimensions = (draw_buffer.width, draw_buffer.height)
                            led_end = to_led_coordinates(chunk.end, led_dimensions)
                            led_start = to_led_coordinates(chunk.start,led_dimensions)

                            vx = SPEED_MULTIPLIER * (led_end[0] - led_start[0]) * 1000 / chunk.elapsed_millis
                            vy = SPEED_MULTIPLIER * (led_end[1] - led_start[1]) * 1000 / chunk.elapsed_millis

                            # Spawn a particle effect that flings a splash of color in the direction of the finger motion
                            emitter = ColorSplashEmitter(led_end[0], led_end[1], vx, vy,
                                                         Rectangle(0, 0, draw_buffer.width, draw_buffer.height))
                            self.emitters.append(emitter)


                    elif event.type == pygame.FINGERMOTION:
                        # Store new chunker
                        self.drag_chunkers[pointer_id] = DragChunker(position_normalized, 200)

        self.emitters = [e for e in self.emitters if e.is_alive()]

        for emitter in self.emitters:
            emitter.update(elapsed_millis)

    def draw(self, draw_buffer: LedDrawBuffer):
        for emitter in self.emitters:
            emitter.draw(draw_buffer)
