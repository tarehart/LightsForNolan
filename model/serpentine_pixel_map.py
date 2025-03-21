class SerpentinePixelMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.serpentine = [[0] * width for _ in range(height)]

        led_index = 0
        for col in range(width):
            serpentine_range = range(height - 1, -1, -1) if col % 2 == 0 else range(height)
            for row in serpentine_range:
                self.serpentine[row][col] = led_index
                led_index += 1

        self.num_pixels = width * height

    def get_pixel_index(self, row: int, col: int) -> int:
        return self.serpentine[row][col]
