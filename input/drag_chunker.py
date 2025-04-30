from dataclasses import dataclass
from typing import Tuple

from particle.cooldown_helper import CooldownHelper

@dataclass
class DragChunk:
    start: Tuple[float, float]
    end: Tuple[float, float]
    elapsed_millis: int



class DragChunker:
    def __init__(self, start_pos: Tuple[float, float],  cooldown_millis):
        self.cooldown = CooldownHelper(cooldown_millis)
        self.drag_start = start_pos
        self.last_pos = start_pos

    def start_drag(self, position: Tuple[float, float]):
        self.drag_start = position
        self.last_pos = position
        self.cooldown.reset()

    def update(self, position: Tuple[float, float], elapsed_millis: int):
        self.last_pos = position
        self.cooldown.update(elapsed_millis)

    def is_chunk_ready(self) -> bool:
        return self.cooldown.is_ready()

    def get_chunk_and_reset(self):
        chunk = DragChunk(self.drag_start, self.last_pos, self.cooldown.elapsed_millis())
        self.start_drag(self.last_pos)
        return chunk

