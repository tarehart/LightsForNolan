from typing import List, Tuple, Dict
import random
import math
import pygame
from pygame.event import EventType
from pygame.time import get_ticks

from draw.led_draw_buffer import LedDrawBuffer
from draw.rainbow_vendor import RainbowVendor
from input.drag_chunker import DragChunker
from model.rectangle import Rectangle
from particle.ripple_particle import RippleParticle
from wled.pixel_push_mode import PixelPushMode


class GridCell:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_color = (0, 0, 0)  # The target color when activated
        self.current_color = (0, 0, 0)  # The current displayed color (for fading)
        self.rainbow_vendor = RainbowVendor(6)
        self.last_activation_time = 0  # When this cell was last activated
        self.fade_duration = 4.0  # Seconds to fade to black
        self.is_being_touched = False  # Whether this cell is currently being touched
        
    def contains_point(self, point: Tuple[float, float]) -> bool:
        """Check if a point is within this cell"""
        return (self.x <= point[0] < self.x + self.width and 
                self.y <= point[1] < self.y + self.height)
    
    def activate(self) -> Tuple[int, int, int]:
        """Activate the cell and return the new color"""
        self.base_color = self.rainbow_vendor.next_color()
        self.current_color = self.base_color
        self.last_activation_time = get_ticks()
        return self.base_color
    
    def update_fade(self):
        """Update the current color based on fade progress and flashing"""
        if self.last_activation_time == 0:
            return
        
        # Calculate base color (fading or full color)
        elapsed_seconds = (get_ticks() - self.last_activation_time) / 1000.0
        base_display_color = self.base_color
        
        if elapsed_seconds >= self.fade_duration:
            # Fully faded to black
            base_display_color = (0, 0, 0)
        else:
            # Calculate fade progress (0 = full color, 1 = black)
            fade_progress = elapsed_seconds / self.fade_duration
            # Linear interpolation from base_color to black
            base_display_color = (
                int(self.base_color[0] * (1 - fade_progress)),
                int(self.base_color[1] * (1 - fade_progress)),
                int(self.base_color[2] * (1 - fade_progress))
            )
        
        # Apply flashing if being touched (4 Hz = 4 cycles per second)
        if self.is_being_touched and base_display_color != (0, 0, 0):
            current_time = get_ticks() / 1000.0
            flash_cycle = (current_time * 4) % 1.0  # 4 Hz
            if flash_cycle < 0.5:
                # Flash to white
                self.current_color = (255, 255, 255)
            else:
                # Show base color
                self.current_color = base_display_color
        else:
            self.current_color = base_display_color
    
    def get_center(self) -> Tuple[float, float]:
        """Get the center point of this cell"""
        return (self.x + self.width / 2, self.y + self.height / 2)


class GridTouchAnimation:
    def __init__(self, bounds: Rectangle, cell_width: int = 3, cell_height: int = 3):
        self.bounds = bounds
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        # Calculate how many cells fit in each dimension
        self.grid_cols = math.ceil(bounds.width / cell_width)
        self.grid_rows = math.ceil(bounds.height / cell_height)
        
        # Initialize grid cells
        self.cells: List[List[GridCell]] = []
        
        for row in range(self.grid_rows):
            cell_row = []
            for col in range(self.grid_cols):
                x = col * cell_width
                y = row * cell_height
                cell = GridCell(x, y, cell_width, cell_height)
                cell_row.append(cell)
            self.cells.append(cell_row)
        
        # Ripple and interaction tracking
        self.ripples: List[RippleParticle] = []
        self.drag_chunkers: Dict[str, DragChunker] = {}
        # Track the last cell interacted with for each pointer to prevent duplicate interactions
        self.last_cell_per_pointer: Dict[str, GridCell] = {}
        
        # Screen dimensions for coordinate conversion
        info = pygame.display.Info()
        self.screen_dimensions = (info.current_w, info.current_h)
        
        # Load bell sound effects
        self.bell_sounds = [
            pygame.mixer.Sound("sounds/bell1.wav"),
            pygame.mixer.Sound("sounds/bell2.wav"),
            pygame.mixer.Sound("sounds/bell3.wav"),
            pygame.mixer.Sound("sounds/bell4.wav")
        ]
        for bell in self.bell_sounds:
            bell.set_volume(0.8)
        
    def get_cell_at_position(self, pos: Tuple[float, float]) -> GridCell | None:
        """Get the grid cell at the given position"""
        for row in self.cells:
            for cell in row:
                if cell.contains_point(pos):
                    return cell
        return None
    
    def spawn_ripple_from_cell(self, cell: GridCell, color: Tuple[int, int, int]):
        """Spawn a ripple from the center of a cell"""
        center = cell.get_center()
        
        ripple = RippleParticle(
            center,
            color,
            (self.bounds.width, self.bounds.height)
        )
        self.ripples.append(ripple)
    
    def handle_interaction(self, pos_normalized: Tuple[float, float], pointer_id: str = "default"):
        """Handle an interaction at the given normalized position"""
        # Convert normalized coordinates to LED coordinates
        led_pos = (
            pos_normalized[0] * self.bounds.width,
            pos_normalized[1] * self.bounds.height
        )
        
        # Find the cell that was touched
        cell = self.get_cell_at_position(led_pos)
        if cell:
            # Check if this cell is already being touched by any pointer
            if cell.is_being_touched:
                return  # Do nothing if cell is already being touched
            
            # Check if this is a different cell than the last one for this pointer
            if pointer_id not in self.last_cell_per_pointer or self.last_cell_per_pointer[pointer_id] != cell:
                # Update the last cell for this pointer
                self.last_cell_per_pointer[pointer_id] = cell
                
                # Activate the cell and get its new color
                new_color = cell.activate()
                
                # Play random bell sound
                random_bell = random.choice(self.bell_sounds)
                random_bell.play()
                
                # Spawn ripple
                self.spawn_ripple_from_cell(cell, new_color)
    
    def update(self, elapsed_millis: int, events: List[EventType], draw_buffer: LedDrawBuffer):
        # Reset all cells' touch status
        for row in self.cells:
            for cell in row:
                cell.is_being_touched = False
        
        # Mark cells that are currently being touched
        for pointer_id, chunker in self.drag_chunkers.items():
            if pointer_id in self.last_cell_per_pointer:
                self.last_cell_per_pointer[pointer_id].is_being_touched = True
        
        # Handle events
        for event in events:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                # Get position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = (event.pos[0] / self.screen_dimensions[0], event.pos[1] / self.screen_dimensions[1])
                    pointer_id = "mouse"
                    # Set up drag tracker for mouse
                    self.drag_chunkers[pointer_id] = DragChunker(pos, 200)
                else:  # FINGERDOWN
                    pos = (event.x, event.y)
                    pointer_id = event.finger_id
                    # Set up drag tracker for finger
                    self.drag_chunkers[pointer_id] = DragChunker(pos, 200)

                self.handle_interaction(pos, pointer_id)

            elif event.type == pygame.MOUSEBUTTONUP and "mouse" in self.drag_chunkers:
                del self.drag_chunkers["mouse"]
                if "mouse" in self.last_cell_per_pointer:
                    del self.last_cell_per_pointer["mouse"]

            elif event.type == pygame.FINGERUP:
                pointer_id = event.finger_id
                if pointer_id in self.drag_chunkers:
                    del self.drag_chunkers[pointer_id]
                if pointer_id in self.last_cell_per_pointer:
                    del self.last_cell_per_pointer[pointer_id]

            elif event.type == pygame.FINGERMOTION or event.type == pygame.MOUSEMOTION:
                pointer_id = None
                position_normalized = None
                if event.type == pygame.FINGERMOTION:
                    pointer_id = event.finger_id
                    position_normalized = (event.x, event.y)
                elif event.type == pygame.MOUSEMOTION:
                    pointer_id = "mouse"
                    position_normalized = (
                        event.pos[0] / self.screen_dimensions[0], 
                        event.pos[1] / self.screen_dimensions[1]
                    )

                if pointer_id is not None and position_normalized is not None:
                    if pointer_id in self.drag_chunkers:
                        chunker = self.drag_chunkers[pointer_id]
                        chunker.update(position_normalized, elapsed_millis)
                        
                        if chunker.is_chunk_ready():
                            chunk = chunker.get_chunk_and_reset()
                            self.handle_interaction(chunk.end, pointer_id)

                    elif event.type == pygame.FINGERMOTION:
                        self.drag_chunkers[pointer_id] = DragChunker(position_normalized, 200)

        # Update cell fading
        for row in self.cells:
            for cell in row:
                cell.update_fade()
        
        # Update ripples
        for ripple in self.ripples:
            ripple.tick()
        
        # Remove ripples that have expired
        self.ripples = [r for r in self.ripples if r.is_alive()]
    
    def draw(self, draw_buffer: LedDrawBuffer) -> PixelPushMode:
        # First, draw the grid cells (background)
        for row in self.cells:
            for cell in row:
                if cell.current_color != (0, 0, 0):  # Only draw non-black cells
                    # Fill the cell with its current color (convert RGB to RGBA)
                    rgba_color = (cell.current_color[0], cell.current_color[1], cell.current_color[2], 255)
                    draw_buffer.fill_rect(cell.x, cell.y, cell.width, cell.height, rgba_color)
        
        # Then draw ripples on top
        for ripple in self.ripples:
            ripple.draw(draw_buffer)
        
        return PixelPushMode.SEND_ALL