from src.ai_agent import AI_Agent
import random
from src.board import Board
from src.game_state import GameState
from src.config import Direction, MOVE_DIRECTIONS, PossibleMoves, GRID_SIZE

class AI_Agent_Random(AI_Agent):
    def choose_best_action(self, board: Board, players, current_player_index):
        state = GameState(board, players, current_player_index, False)
        actions = state.generate_possible_moves(current_player_index, players)
        if not actions:
            return PossibleMoves.NOTHING
        return random.choice(actions)