import pygame

from src.ai_agent_minmax import AI_AgentMinMax, AI_AgentAlphaBeta, AI_agent
from src.board import Board
from src.draw import Draw
from src.game import Game
from src.player import Player
from src.config import screen, RED, GREEN, BLUE, YELLOW, Direction

# Initialize Pygame
pygame.init()


if __name__ == "__main__":
    board = Board()
    ai_agent_minmax_depth2: AI_agent = AI_AgentMinMax(2)
    ai_agent_minmax_depth1: AI_agent = AI_AgentMinMax(1)
    ai_agent_alpha_beta_depth4: AI_agent = AI_AgentAlphaBeta(4)
    ai_agent_alpha_beta_depth5: AI_agent = AI_AgentAlphaBeta(5)
    ai_agent_alpha_beta_depth3: AI_agent = AI_AgentAlphaBeta(3)
    ai_agent_alpha_beta_depth2: AI_agent = AI_AgentAlphaBeta(2)
    players = [
        Player(RED, "Red", Direction.UP, player_is_AI=True, ai_agent=ai_agent_minmax_depth1),  # Red
        Player(GREEN, "Green", Direction.DOWN, player_is_AI=True, ai_agent=ai_agent_alpha_beta_depth4),  # Green
        Player(BLUE, "Blue", Direction.LEFT, player_is_AI=True, ai_agent=ai_agent_alpha_beta_depth5),  # Blue
        Player(YELLOW, "Yellow", Direction.RIGHT, player_is_AI=True, ai_agent=ai_agent_alpha_beta_depth2)  # Yellow
    ]
    players1 = [
        Player(RED, "Red", Direction.UP, player_is_AI=True, ai_agent=ai_agent_alpha_beta_depth2),  # Red
        Player(GREEN, "Green", Direction.DOWN, player_is_AI=True, ai_agent=ai_agent_alpha_beta_depth4)  # Yellow
    ]

    players2 = [
        Player(RED, "Red", Direction.UP),  # Red
        Player(GREEN, "Green", Direction.DOWN),  # Green
        Player(BLUE, "Blue", Direction.LEFT),  # Blue
        Player(YELLOW, "Yellow", Direction.RIGHT)  # Yellow
    ]
    draw = Draw(screen)
    game = Game(screen, players, board, draw)
    game.run()
