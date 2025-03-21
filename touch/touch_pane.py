import pygame

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class TouchPane:

    def __init__(self):

        # Initialize Pygame
        pygame.init()

        # Set up fullscreen window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Touch Drawing Test")

        # Store previous touch positions
        self.finger_positions = {}

        self.running = True


    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Detect touchscreen movements
            elif event.type == pygame.FINGERMOTION:
                finger_id = event.finger_id  # Track individual fingers
                x, y = event.x * self.screen.get_width(), event.y * self.screen.get_height()

                if finger_id in self.finger_positions:
                    # Draw a line from previous position to current position
                    pygame.draw.line(self.screen, WHITE, self.finger_positions[finger_id], (x, y), 5)

                # Store new position
                self.finger_positions[finger_id] = (x, y)

            # Remove finger from tracking when lifted
            elif event.type == pygame.FINGERUP:
                if event.finger_id in self.finger_positions:
                    del self.finger_positions[event.finger_id]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_c:  # Press 'C' to clear the screen
                    self.screen.fill(BLACK)

        pygame.display.flip()


