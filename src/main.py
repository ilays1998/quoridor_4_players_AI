import pygame

from src.board import Board
from src.draw import Draw
from src.game import Game
from src.config import screen
# Initialize Pygame
pygame.init()


if __name__ == "__main__":
    board = Board()

    draw = Draw(screen)
    game = Game(screen, board, draw)
    game.run()
