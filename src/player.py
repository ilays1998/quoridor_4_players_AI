import pygame

from src.ai_agent_minmax import AI_AgentAlphaBeta
from src.ai_agent_montecarlo import AI_Agent_MonteCarlo
from src.ai_agent_random import AI_Agent_Random
from src.config import SQUARE_SIZE, CONSOLE_WIDTH, screen, GRID_SIZE, Direction, RED, GREEN, BLUE, YELLOW, COLOR_NAMES
import random



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


class Player:
    def __init__(self, color, name, direction=None, x=0, y=0, player_is_AI=False, ai_agent=None):
        self.goal = None
        if direction is None:
            self.x, self.y = x, y
        else:
            self.x, self.y = direction.value
            self.goal = set_goal(direction)
        self.walls_left = 5
        self.color = color
        self.name = name
        self.player_is_AI: bool = player_is_AI
        self.ai_agent = ai_agent


    def get_position(self):
        return self.x, self.y


class PlayerFactory:
    used_colors = set()
    used_directions = set()
    colors = [RED, GREEN, BLUE, YELLOW]
    directions_for_4 = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    directions_for_2 = [Direction.UP, Direction.DOWN]
    ai_agents = [AI_AgentAlphaBeta(2) for _ in range(4)]
    # ai_agents = [AI_Agent_MonteCarlo(1000, 2) for _ in range(4)]

    @staticmethod
    def get_player(player_is_AI, num_players=4):
        available_colors = [color for color in PlayerFactory.colors if color not in PlayerFactory.used_colors]
        if num_players == 2:
            available_directions = [direction for direction in PlayerFactory.directions_for_2 if direction not in PlayerFactory.used_directions]
        else:
            available_directions = [direction for direction in PlayerFactory.directions_for_4 if direction not in PlayerFactory.used_directions]

        if not available_colors or not available_directions:
            raise ValueError("No available colors or directions left")

        color = random.choice(available_colors)
        direction = random.choice(available_directions)

        PlayerFactory.used_colors.add(color)
        PlayerFactory.used_directions.add(direction)
        ai_agent = PlayerFactory.ai_agents.pop() if player_is_AI else None

        return Player(color, f"{COLOR_NAMES[color]}", direction, player_is_AI=player_is_AI, ai_agent=ai_agent)
