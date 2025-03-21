import socket
from typing import List, Tuple

from model.indexed_pixel import IndexedPixel


class WledInterface:
    WARLS_FORMAT = 1
    DRGB_FORMAT = 2

    def __init__(self, ip_address: str, udp_port: int):
        self.address = (ip_address, udp_port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_specific_pixels(self, pixels: List[IndexedPixel], seconds_to_persist: int = 10):
        assert 0 <= seconds_to_persist <= 255, "seconds_to_persist must be between 0 and 255"

        # Prepare the byte array
        bytes_data = bytearray([self.WARLS_FORMAT, seconds_to_persist])

        for pixel in pixels:
            bytes_data.append(pixel.index)
            bytes_data.append(pixel.color[0])  # Unpack (R, G, B)
            bytes_data.append(pixel.color[1])
            bytes_data.append(pixel.color[2])

        # Send packet
        self.udp_socket.sendto(bytes_data, self.address)

    def send_all_pixels(self, pixels: List[Tuple[int, int, int]], seconds_to_persist: int = 10):
        assert 0 <= seconds_to_persist <= 255, "seconds_to_persist must be between 0 and 255"

        # Prepare the byte array
        bytes_data = bytearray([self.DRGB_FORMAT, seconds_to_persist])

        for color in pixels:
            bytes_data.extend(color)  # Unpack (R, G, B)

        # Send packet
        self.udp_socket.sendto(bytes_data, self.address)
