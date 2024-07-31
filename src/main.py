import pygame

from src.ai_agent_minmax import AI_AgentMinMax
from src.board import Board
from src.draw import Draw
from src.game import Game
from src.player import Player
from src.config import screen, RED, GREEN, BLUE, YELLOW, Direction

# Initialize Pygame
pygame.init()


if __name__ == "__main__":
    board = Board()
    ai_agent = AI_AgentMinMax(2)
    players = [
        Player(RED, "Red", Direction.UP),  # Red
        Player(GREEN, "Green", Direction.DOWN, player_is_AI=True),  # Green
        Player(BLUE, "Blue", Direction.LEFT),  # Blue
        Player(YELLOW, "Yellow", Direction.RIGHT)  # Yellow
    ]
    draw = Draw(screen)
    game = Game(screen, players, board, draw, ai_agent)
    game.run()
