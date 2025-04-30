class SerpentinePixelMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.serpentine = [[0] * width for _ in range(height)]

        led_index = 0
        for row in range(height-1, -1, -1):
            if (height - 1 - row) % 2 == 0:
                serpentine_range = range(width-1, -1, -1)  # right to left
            else:
                serpentine_range = range(width)  # left to right
            for col in serpentine_range:
                self.serpentine[row][col] = led_index
                led_index += 1

        self.num_pixels = width * height

        self.print_map()

    def get_pixel_index(self, row: int, col: int) -> int:
        return self.serpentine[row][col]


    def print_map(self):
        max_index = self.num_pixels - 1
        width = len(str(max_index))  # Number of digits in the largest index
        for row in self.serpentine:
            print(" ".join(f"{idx:{width}}" for idx in row))
