import copy

from src.board import Board
from src.config import Direction, PossibleMoves, MOVE_DIRECTIONS, GRID_SIZE


class GameState:

    def __init__(self, board: Board, players, current_player_index, game_over):
        self.board = copy.deepcopy(board)
        self.players = copy.deepcopy(players)
        self.players_goal_positions = {player: self.board.get_goal_positions(player.goal)
                                       for player in players}
        self.current_player_index = current_player_index
        self.game_over = game_over

    def __str__(self):
        result = ""
        for index, player in enumerate(self.players):
            result += f"player {index}: {player.get_position()}\n"

        for i in range(GRID_SIZE):
            result += '\n'
            for j in range(GRID_SIZE):
                if i < GRID_SIZE - 1 and j < GRID_SIZE - 1:

                    if self.board.v_walls[i][j]:
                        result += ("|| ")
                    else:
                        result += ("| ")
                    if self.board.h_walls[i][j]:
                        result += "="
                    else:
                        result += "-"
                else:
                    result += "-  "
                for index, player in enumerate(self.players):
                    if player.get_position()[0] == i and player.get_position()[1] == j:
                        result += str(index)

        result += "\n\n"
        return result

    def generate_possible_moves(self, player_index: int, other_players: list):
        moves = []
        player = self.players[player_index]
        # Add pawn movements using Direction enum
        for direction, (dx, dy) in MOVE_DIRECTIONS.items():
            new_x, new_y = player.x + dx, player.y + dy
            if self.board.is_move_legal(new_x, new_y, other_players, direction, player, jump=False):

                for p in other_players:  # jump above players
                    if (p.x == new_x
                            and p.y == new_y):
                        if not self.board.check_win_condition(player.goal, new_x, new_y):
                            new_x += dx
                            new_y += dy
                            break
                moves.append((PossibleMoves.MOVE, new_x,
                              new_y,
                              direction))

        # Add wall placements
        if player.walls_left == 0:
            return moves
        for x in range(GRID_SIZE - 1):
            for y in range(GRID_SIZE - 1):
                for orientation in ['h', 'v']:
                    if self.board.can_place_wall(x, y, orientation, other_players):
                        moves.append((PossibleMoves.WALL, x, y, orientation))

        return moves

    def apply_move(self, move: tuple):
        if self.game_over:
            return None
        successor = GameState(self.board, self.players, self.current_player_index, self.game_over)
        if move[0] == PossibleMoves.MOVE:
            new_x, new_y, direction = move[1], move[2], move[3]
            player = successor.players[successor.current_player_index]
            player.x = new_x
            player.y = new_y
            if successor.board.check_win_condition(player.goal, player.x, player.y):
                successor.game_over = True
            successor.current_player_index = (successor.current_player_index + 1) % len(successor.players)
        elif move[0] == PossibleMoves.WALL:
            x, y, orientation = move[1], move[2], move[3]
            successor.board.set_wall(x, y, orientation)
            successor.players[successor.current_player_index].walls_left -= 1
            successor.current_player_index = (successor.current_player_index + 1) % len(successor.players)

        return successor

    def hash(self):
        # Create a unique hash based on the board state and player positions
        board_hash = hash(str(self.board))
        player_positions_hash = hash(tuple((player.x, player.y) for player in self.players))
        return hash((board_hash, player_positions_hash, self.current_player_index))

    def get_winner(self):
        """
        get the winner of the match. return None if match not over
        :return: index of winner if game over, -1 if not
        """
        if not self.game_over:
            return -1
        return (self.current_player_index - 1) % (len(self.players))
