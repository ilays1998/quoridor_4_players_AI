# config.py
import pygame
from enum import Enum

# Initialize Pygame screen here or just define the constants and initialize the screen elsewhere
# Screen dimensions
BOARD_SIZE = 600
BOARD_WIDTH, BOARD_HEIGHT = BOARD_SIZE, BOARD_SIZE
CONSOLE_WIDTH = 200
SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH + CONSOLE_WIDTH, BOARD_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GRID_COLOR = (200, 200, 200)  # Light grey
LIGHT_WHITE = (220, 220, 220)  # Lighter shade of white, less glow

# Board settings
GRID_SIZE = 9
SQUARE_SIZE = BOARD_WIDTH // GRID_SIZE
WALL_THICKNESS = 5


class Direction(Enum):
    UP = GRID_SIZE // 2, 0
    DOWN = GRID_SIZE // 2, GRID_SIZE - 1
    LEFT = 0, GRID_SIZE // 2
    RIGHT = GRID_SIZE - 1, GRID_SIZE // 2

    __getitem__ = Enum.__getitem__  # Add this line to allow indexing Direction enum by integer


MOVE_DIRECTIONS = {
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
}


class PossibleMoves(Enum):
    MOVE = 1
    WALL = 2
    NOTHING = 3

