import copy

import pygame
import sys

from src.config import CONSOLE_WIDTH, GRID_SIZE, SQUARE_SIZE, Direction, MOVE_DIRECTIONS, PossibleMoves
from src.player import Player


class Game:
    def __init__(self, screen, players, board, draw, ai_agent):
        self.screen = screen
        self.players = players
        self.board = board
        self.current_player_index = 0
        self.selected_orientation = 'h'
        self.draw = draw
        self.clock = pygame.time.Clock()
        self.ai_agent = ai_agent

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

    @staticmethod
    def handle_quit_event(event):
        pygame.quit()
        sys.exit()

    def handle_mouse_button_down(self, event):  # return True if place a wall
        mouse_x, mouse_y = event.pos

        # Check if click is in console area
        if mouse_x < CONSOLE_WIDTH:
            self.handle_console_click(mouse_y)
            return False
        else:
            return self.handle_wall_placement(mouse_x, mouse_y)

    def handle_console_click(self, mouse_y):
        if 60 <= mouse_y <= 110:
            self.selected_orientation = 'h'
        elif 120 <= mouse_y <= 170:
            self.selected_orientation = 'v'

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

    def handle_key_down(self, event):
        current_player = self.players[self.current_player_index]
        key_to_move = {
            pygame.K_UP: ((0, -1), Direction.UP),
            pygame.K_DOWN: ((0, 1), Direction.DOWN),
            pygame.K_LEFT: ((-1, 0), Direction.LEFT),
            pygame.K_RIGHT: ((1, 0), Direction.RIGHT),
        }
        if event.key in key_to_move:
            move, direction = key_to_move[event.key]
            return self.handle_player_move(current_player, move, direction)
        return False

    def handle_player_move(self, current_player, move, direction):
        new_x, new_y = current_player.x + move[0], current_player.y + move[1]
        player_jump_to_win = False

        for player in self.players:
            if player.x == new_x and player.y == new_y:
                if self.board.is_move_legal(new_x, new_y, [], direction, jump=False):
                    if self.board.check_win_condition(current_player.goal, new_x, new_y):
                        player_jump_to_win = True
                    else:
                        new_x += move[0]
                        new_y += move[1]
                break

        if player_jump_to_win or self.board.is_move_legal(new_x, new_y, self.players, direction, jump=True):
            self.draw.draw_pseudo_move(Player((128, 128, 128), "pseudo", x=new_x, y=new_y), current_player,
                                       self.selected_orientation)
            self.draw.update_screen()
            next_event = self.wait_for_next_event()
            if next_event.type == pygame.KEYDOWN and next_event.key == pygame.K_RETURN:
                self.finalize_player_move(current_player, new_x, new_y)
                return True
        return False

    @staticmethod
    def wait_for_next_event():
        while True:
            event = pygame.event.wait()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return event

    def finalize_player_move(self, current_player, new_x, new_y):
        current_player.x, current_player.y = new_x, new_y

    def next_player_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def decrease_num_player_wall(self, current_player):
        current_player.walls_left -= 1

    def player_win(self, current_player):
        self.draw.draw_winner_message(self.board, self.players, current_player)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw.update_screen()
            self.clock.tick(60)

    def run(self):
        while True:
            current_player = self.players[self.current_player_index]
            action = PossibleMoves.NOTHING
            if current_player.player_is_AI:
                # make best move for AI player
                best_move = self.ai_agent.choose_best_move(
                    (self.board, self.players, self.current_player_index, self.current_player_index, False))
                # this is only return the move
                action = best_move[0]
                if action == PossibleMoves.MOVE:
                    self.finalize_player_move(current_player, best_move[3], best_move[4])
                elif action == PossibleMoves.WALL:
                    self.board.set_wall(best_move[1], best_move[2], best_move[3])

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.handle_quit_event(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.handle_mouse_button_down(event):
                            action = PossibleMoves.WALL
                    elif event.type == pygame.KEYDOWN:
                        if self.handle_key_down(event):
                            action = PossibleMoves.MOVE

            if not action == PossibleMoves.NOTHING:
                if action == PossibleMoves.MOVE and self.board.check_win_condition(current_player.goal,
                                                                                   current_player.x, current_player.y):
                    self.player_win(current_player)
                if action == PossibleMoves.WALL:
                    self.decrease_num_player_wall(current_player)
                self.next_player_turn()

            # and then check if the player wins (human or AI)

            self.draw.draw_game_screen(self.board, self.players, self.current_player_index, self.selected_orientation)
            self.draw.update_screen()
            self.clock.tick(60)
