import abc
from src.board import Board

class AI_Agent:
    @abc.abstractmethod
    def choose_best_action(self, board: Board, players, current_player_index):
        return