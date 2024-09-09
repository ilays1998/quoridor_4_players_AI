import copy

import pygame
import sys
import time

from src.ai_agent_minmax import EvaluationFunction
from src.config import CONSOLE_WIDTH, GRID_SIZE, SQUARE_SIZE, Direction, MOVE_DIRECTIONS, PossibleMoves
from src.player import Player, PlayerFactory
from src.ai_agent_minmax import AI_AgentMinMax, AI_AgentAlphaBeta, AI_agent
from src.config import RED, GREEN, BLUE, YELLOW, Direction

class AI_Game:
    def __init__(self, board, players):
        self.players = players
        self.board = board
        self.current_player_index = 0
        self.selected_orientation = 'h'
        self.winner = None

    @staticmethod
    def calculate_grid_position(mouse_x, mouse_y):
        grid_x = (mouse_x - CONSOLE_WIDTH) // SQUARE_SIZE
        grid_y = mouse_y // SQUARE_SIZE
        if mouse_y % SQUARE_SIZE < SQUARE_SIZE // 2:
            if grid_y > 0:
                grid_y -= 1
        if (mouse_x - CONSOLE_WIDTH) % SQUARE_SIZE < SQUARE_SIZE // 2:
            if grid_x > 0:
                grid_x -= 1
        return grid_x, grid_y

    def handle_wall_placement(self, mouse_x, mouse_y):
        if self.players[self.current_player_index].walls_left > 0:
            grid_x, grid_y = self.calculate_grid_position(mouse_x, mouse_y)
            if self.selected_orientation == 'h' and grid_y >= GRID_SIZE - 1:
                return False
            elif self.selected_orientation == 'v' and grid_x >= GRID_SIZE - 1:
                return False
            if self.board.place_wall(grid_x, grid_y, self.selected_orientation, self.players):
                return True
        return False

    def handle_player_move(self, current_player, move, direction):
        new_x, new_y = current_player.x + move[0], current_player.y + move[1]
        player_jump_to_win = False

        for player in self.players:
            if player.x == new_x and player.y == new_y:
                if self.board.is_move_legal(new_x, new_y, [], direction, current_player, jump=False):
                    if self.board.check_win_condition(current_player.goal, new_x, new_y):
                        player_jump_to_win = True
                    else:
                        new_x += move[0]
                        new_y += move[1]
                break

        if player_jump_to_win or self.board.is_move_legal(new_x, new_y, self.players, direction, current_player,
                                                          jump=True):
            self.finalize_player_move(current_player, new_x, new_y)
        return False

    def finalize_player_move(self, current_player, new_x, new_y):
        current_player.x, current_player.y = new_x, new_y

    def next_player_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def decrease_num_player_wall(self, current_player):
        current_player.walls_left -= 1

    def print_distances_to_goal(self):
        for player in self.players:
            distance = EvaluationFunction.a_star_path_length(self.board, player)
            print(f"Player {player.name} distance to goal: {distance}")

    def run(self):
        while True:
            current_player = self.players[self.current_player_index]
            # action = PossibleMoves.NOTHING

            # self.print_distances_to_goal()
            # make best move for AI player
            best_move = current_player.ai_agent.choose_best_action(self.board, self.players,
                                                                   self.current_player_index)
            action = best_move[0]
            if action == PossibleMoves.MOVE:
                self.finalize_player_move(current_player, best_move[1], best_move[2])
            elif action == PossibleMoves.WALL:
                self.board.set_wall(best_move[1], best_move[2], best_move[3])

            if action == PossibleMoves.MOVE and self.board.check_win_condition(current_player.goal,
                                                                               current_player.x, current_player.y):
                self.winner = current_player
                return
            if action == PossibleMoves.WALL:
                self.decrease_num_player_wall(current_player)
            self.next_player_turn()