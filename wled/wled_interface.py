import socket
from typing import List, Tuple

import pygame

from model.serpentine_pixel_map import SerpentinePixelMap


class WledInterface:
    WARLS_FORMAT = 1
    DRGB_FORMAT = 2

    def __init__(self, ip_address: str, udp_port: int, pixel_map: SerpentinePixelMap):
        self.address = (ip_address, udp_port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.pixel_map = pixel_map

    def send_opaque_pixels(self, surface: pygame.Surface, seconds_to_persist: int = 10):
        assert 0 <= seconds_to_persist <= 255, "seconds_to_persist must be between 0 and 255"

        # Prepare the byte array
        bytes_data = bytearray([self.WARLS_FORMAT, seconds_to_persist])

        # Extract and send only non-transparent pixels
        for row in range(self.pixel_map.height):
            for col in range(self.pixel_map.width):
                index = self.pixel_map.get_pixel_index(row, col)
                color = surface.get_at((col, row))
                if color[3] > 0:  # Check alpha value
                    bytes_data.append(index)
                    bytes_data.extend(color[:3])  # Extract (R, G, B)

        # Send packet
        self.udp_socket.sendto(bytes_data, self.address)


    def send_all_pixels(self, surface: pygame.Surface, seconds_to_persist: int = 10):
        assert 0 <= seconds_to_persist <= 255, "seconds_to_persist must be between 0 and 255"

        # Pre-allocate the byte array
        bytes_data = bytearray(2 + self.pixel_map.width * self.pixel_map.height * 3)
        bytes_data[0] = self.DRGB_FORMAT
        bytes_data[1] = seconds_to_persist

        # Extract pixel data and reorder based on the serpentine mapping
        for row in range(self.pixel_map.height):
            for col in range(self.pixel_map.width):
                index = self.pixel_map.get_pixel_index(row, col)
                color = surface.get_at((col, row))[:3]  # Extract (R, G, B) only
                pixel_offset = 2 + index * 3
                bytes_data[pixel_offset:pixel_offset + 3] = color

        # Send packet
        self.udp_socket.sendto(bytes_data, self.address)

    def send_pixel_indices(self, indices: List[int], color: Tuple[int, int, int]):
        """
        This is for diagnostic purposes
        """

        # Pre-allocate the byte array
        bytes_data = bytearray(2 + self.pixel_map.width * self.pixel_map.height * 3)
        bytes_data[0] = self.DRGB_FORMAT
        bytes_data[1] = 10

        # Extract pixel data and reorder based on the serpentine mapping
        for index in indices:
            pixel_offset = 2 + index * 3
            bytes_data[pixel_offset:pixel_offset + 3] = color[:3]

        # Send packet
        self.udp_socket.sendto(bytes_data, self.address)
