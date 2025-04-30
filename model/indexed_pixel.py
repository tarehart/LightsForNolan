from dataclasses import dataclass
from typing import Tuple


@dataclass
class IndexedPixel:
    index: int
    color: Tuple[int, int, int, int]  # (R, G, B, A)