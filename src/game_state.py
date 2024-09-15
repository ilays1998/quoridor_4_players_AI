import copy
from typing import Optional

from src.board import Board
from src.config import PossibleMoves, MOVE_DIRECTIONS, GRID_SIZE, Direction
from collections import deque


class GameState:
    WALL_SEARCH_DEF = 1

    def __init__(self, board: Board, players, current_player_index, game_over):
        self.board = copy.deepcopy(board)
        self.players = copy.deepcopy(players)
        self.players_goal_positions = {player: self.board.get_goal_positions(player.goal)
                                       for player in players}
        self.current_player_index = current_player_index
        self.game_over = game_over
        # self.visited_already = [[[False for _ in range(GRID_SIZE)]
        #                          for _ in range(GRID_SIZE)] for player in players]
        # self.new_players_goal_positions = {i: self.board.get_goal_positions(player.goal)
        #                                for i, player in enumerate(players)}

    def __str__(self):
        # print("players goal position: ",self.players_goal_positions,"\n")
        # print([player.get_position() for player in self.players])
        # print("\n")
        lines = []
        for _ in range(GRID_SIZE):
            lines.append(["+---"] * GRID_SIZE + ["+"])
            lines.append(["|   "] * GRID_SIZE + ["|"])
        lines.append(["+---"] * GRID_SIZE + ["+"])

        for i in range(GRID_SIZE - 1):
            for j in range(GRID_SIZE - 1):
                if self.board.v_walls[i][j]:
                    lines[i * 2 + 1][j + 1] = "‖   "
                    lines[i * 2 + 3][j + 1] = "‖   "
                if self.board.h_walls[i][j]:
                    lines[i * 2 + 2][j] = "+==="
                    lines[i * 2 + 2][j + 1] = "+==="

        for player_index, player in enumerate(self.players):
            x, y = player.get_position()
            # print(player.get_position())
            prev_line = lines[y * 2 + 1][x]
            lines[y * 2 + 1][x] = prev_line[:2] + f"{player_index}" + prev_line[2]

        return "\n".join(["".join(line) for line in lines]) + "\n"

    def get_shortest_path_move(self, player_index):
        player = self.players[player_index]
        start_x, start_y = player.x, player.y
        goal_positions = self.new_players_goal_positions[player_index]

        # BFS setup
        queue = deque([(start_x, start_y, None)])  # (x, y, first_move)
        visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        visited[start_x][start_y] = True

        while queue:
            x, y, first_move = queue.popleft()

            # Debug: Print current position
            # print(f"BFS exploring position: ({x}, {y})")

            # Check if we reached a goal
            if (x, y) in goal_positions:
                # print(f"Found goal at: ({x}, {y})")
                return first_move  # Return the first move of the path

            # Generate possible moves from this position
            for move_type, new_x, new_y, direction in self.generate_possible_moves(player_index, self.players):
                if not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, first_move or direction))
        # print(self)
        # print("No moves found in BFS")
        return None

























    def generate_probable_moves(self, player_index: int, other_players: list):
        probobal_moves = list()
        player = self.players[player_index]
        # Add pawn movements using Direction enum
        for direction, (dx, dy) in MOVE_DIRECTIONS.items():
            new_x, new_y = player.x + dx, player.y + dy
            if self.board.is_move_legal(new_x, new_y, other_players, direction, player, jump=False):
                for p in other_players:  # jump above players
                    if p.x == new_x and p.y == new_y:
                        if not self.board.check_win_condition(player.goal, new_x, new_y):
                            new_x += dx
                            new_y += dy
                            break
                move = (PossibleMoves.MOVE, new_x, new_y, direction)
                probobal_moves.append(move)
                # if not self.visited_already[self.current_player_index][new_x][new_y]:
                #     probobal_moves.add((PossibleMoves.MOVE, new_x,
                #               new_y,
                #               direction)) #we don't want to visit somewhere we already was in
        # if len(probobal_moves) == 0:
        #     #we couldnt go somwhere else, add somewhere we already been to
        #     print(self)
        #     print(self.game_over)
        #     for direction, (dx, dy) in MOVE_DIRECTIONS.items():
        #         new_x, new_y = player.x + dx, player.y + dy
        #         print(direction, " is legal: ",
        #               self.board.is_move_legal(new_x, new_y, other_players, direction, player, jump=False))

        # Add wall placements, in proboable - only walls close to me or my enemies
        if player.walls_left == 0:
            return probobal_moves
        for player in other_players:
            for x in range(-GameState.WALL_SEARCH_DEF, GameState.WALL_SEARCH_DEF):
                for y in range(-GameState.WALL_SEARCH_DEF, GameState.WALL_SEARCH_DEF):
                    for orientation in ['h', 'v']:
                        if self.board.can_place_wall(player.x + x, player.y + y, orientation, other_players):
                            move = (PossibleMoves.WALL, player.x + x, player.y + y, orientation)
                            probobal_moves.append(move)

        return probobal_moves

    def generate_possible_moves(self, player_index: int, other_players: list):
        moves = []
        player = self.players[player_index]

        # Add pawn movements using Direction enum
        for direction, (dx, dy) in MOVE_DIRECTIONS.items():
            new_x, new_y = player.x + dx, player.y + dy

            if self.board.is_move_legal(new_x, new_y, other_players, direction, player, jump=False):
                # Check if another player is in the way
                for p in other_players:
                    if p.x == new_x and p.y == new_y:
                        new_x += dx
                        new_y += dy
                        break

                moves.append((PossibleMoves.MOVE, new_x, new_y, direction))

        # Add wall placements
        if player.walls_left > 0:
            for x in range(GRID_SIZE - 1):
                for y in range(GRID_SIZE - 1):
                    for orientation in ['h', 'v']:
                        if self.board.can_place_wall(x, y, orientation, other_players):
                            moves.append((PossibleMoves.WALL, x, y, orientation))

        # Debug: Print possible moves
        # print(f"Possible moves for player {player_index}: {moves}")
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

    def apply_move_no_cpy(self, move: tuple):
        # if self.board.is_move_legal(move[1],move[2],self.players,move[3], self.current_player_index, jump=False)
        if self.game_over:
            return None
        if move[0] == PossibleMoves.MOVE:
            new_x, new_y, direction = move[1], move[2], move[3]
            player = self.players[self.current_player_index]
            player.x = new_x
            player.y = new_y
            # self.visited_already[self.current_player_index][new_x][new_y] = True
            #add to the list of already visited
            if self.board.check_win_condition(player.goal, player.x, player.y):
                self.game_over = True
        elif move[0] == PossibleMoves.WALL:
            x, y, orientation = move[1], move[2], move[3]
            self.board.set_wall(x, y, orientation)
            self.players[self.current_player_index].walls_left -= 1
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        return self

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
        # print("goal for each player is:")
        # for i in range(len(self.players)):
        #     print("player number is: ", i, "player goal is: ", self.players[i].goal, "player position is: ",
        #           self.players[i].get_position())
        # print(self)
        # print("winner is: ", (self.current_player_index - 1) % (len(self.players)))
        return (self.current_player_index - 1) % (len(self.players))