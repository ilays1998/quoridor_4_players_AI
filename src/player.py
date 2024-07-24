import pygame
from src.config import SQUARE_SIZE, CONSOLE_WIDTH, screen, GRID_SIZE, Direction


# Player class
def set_goal(direction):
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.UP
    if direction == Direction.RIGHT:
        return Direction.LEFT
    if direction == Direction.LEFT:
        return Direction.RIGHT


# TODO: draw as static function that get Player as parameter
class Player:
    def __init__(self, color, name, direction=None, x=0, y=0):
        self.goal = None
        if direction is None:
            self.x, self.y = x, y
        else:
            self.x, self.y = direction.value
            self.goal = set_goal(direction)
        self.walls_left = 5
        self.color = color
        self.name = name

    def get_position(self):
        return self.x, self.y

