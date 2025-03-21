from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
from model.indexed_pixel import IndexedPixel
from model.serpentine_pixel_map import SerpentinePixelMap


class LedDrawBuffer:
    def __init__(self, pixel_map: SerpentinePixelMap):
        self.pixel_map = pixel_map
        self.width = pixel_map.width
        self.height = pixel_map.height

        # Create an image with an RGBA mode
        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def draw_image(self, image: Image, x: int = 0, y: int = 0, width: int = None, height: int = None):
        """Draw another image onto this one."""
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        image = image.resize((width, height))
        self.image.paste(image, (x, y))


    def draw_line(self, start: Tuple[int, int], end: Tuple[int, int], color: Tuple[int, int, int]):
        self.draw.line([start, end], color)

    def fill_rect(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int, int]):
        """Fill a rectangle with a given color."""
        self.draw.rectangle([x, y, x + width - 1, y + height - 1], fill=color)

    def draw_text(self, text: str, x: int, y: int, color: Tuple[int, int, int, int], size: int):
        """Draw text at a specific location."""
        try:
            font = ImageFont.truetype("arial.ttf", size)
        except IOError:
            font = ImageFont.load_default()
        self.draw.text((x, y), text, font=font, fill=color)

    def clear_all(self, color: Tuple[int, int, int, int] = (0, 0, 0, 255)):
        """Clear the entire buffer with a given color."""
        self.fill_rect(0, 0, self.width, self.height, color)

    def get_all_pixels(self) -> List[IndexedPixel]:
        """Retrieve all pixels from the image as IndexedPixel objects."""
        pixels = self.image.getdata()

        return [
            IndexedPixel(self.pixel_map.get_pixel_index(row, col), pixels[index])
            for index, (col, row) in enumerate(
                ((i % self.width, i // self.width) for i in range(len(pixels)))
            )
        ]

    def get_opaque_pixels(self) -> List[IndexedPixel]:
        """Retrieve only non-transparent pixels."""
        all_pixels = self.get_all_pixels()
        return [px for px in all_pixels if px.color[3] > 0]
