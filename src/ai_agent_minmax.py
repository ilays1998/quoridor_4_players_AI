from src.board import Board
from src.config import GRID_SIZE, MOVE_DIRECTIONS
from src.game_state import GameState


class EvaluationFunction:

    @staticmethod
    def bfs_path_length(board, player):
        from collections import deque

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (player.x, player.y)
        goal_positions = board.get_goal_positions(player.goal)
        queue = deque([(start, 0)])  # (position, path_length)
        visited = set([start])

        while queue:
            (x, y), path_length = queue.popleft()
            if (x, y) in goal_positions:
                return float('-inf') if path_length == 0 else path_length

            for direction, (dx, dy) in MOVE_DIRECTIONS.items():
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited:
                    if board.is_move_legal(neighbor[0], neighbor[1], [], direction, player, jump=False):
                        queue.append((neighbor, path_length + 1))
                        visited.add(neighbor)

        return float("inf")

    @staticmethod
    def a_star_path_length(board, player):
        from queue import PriorityQueue

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (player.x, player.y)
        goal_positions = board.get_goal_positions(player.goal)
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {node: float("inf") for node in
                   [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
        g_score[start] = 0
        f_score = {node: float("inf") for node in
                   [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
        f_score[start] = min(heuristic(start, goal) for goal in goal_positions)

        while not open_set.empty():
            current = open_set.get()[1]

            if current in goal_positions:
                total_path = [current]
                while current in came_from:
                    current = came_from[current]
                    total_path.append(current)
                path_length = len(total_path) - 1
                return path_length

            for direction, (dx, dy) in MOVE_DIRECTIONS.items():
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                    if board.is_move_legal(neighbor[0], neighbor[1], [], direction, player, jump=False):
                        tentative_g_score = g_score[current] + 1
                        if tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] + min(
                                heuristic(neighbor, goal) for goal in goal_positions)
                            if not any(neighbor == item[1] for item in open_set.queue):
                                open_set.put((f_score[neighbor], neighbor))
                        else:
                            pass

        return float("inf")

    @staticmethod
    def evaluate(state: GameState, AI_player_index):
        ai_player = state.players[AI_player_index]
        ai_distance = EvaluationFunction.a_star_path_length(state.board, ai_player)

        other_players_distance = 0
        for i, player in enumerate(state.players):
            if i != AI_player_index:
                other_players_distance += EvaluationFunction.a_star_path_length(state.board, player)

        return ai_distance - other_players_distance


class AI_AgentMinMax:

    def __init__(self, depth):
        self.depth = depth

    def minimax(self, state: GameState, depth, player_index):
        if depth == 0:
            return EvaluationFunction.evaluate(state, player_index), None

        actions = state.generate_possible_moves(state.current_player_index)
        print("Possible moves:", actions)
        best_action = None

        if player_index != 0:
            best_value = float('-inf')
            for action in actions:
                successor = state.apply_move(action)
                if successor.game_over:
                    return EvaluationFunction.evaluate(state, player_index), action
                new_value, _ = self.minimax(successor, depth - 1, player_index)
                if new_value > best_value:
                    best_value, best_action = new_value, action
        else:
            best_value = float('inf')
            for action in actions:
                successor = state.apply_move(action)
                if successor.game_over:
                    return EvaluationFunction.evaluate(state, player_index), action
                new_value, _ = self.minimax(successor, depth - 1, player_index)
                if new_value < best_value:
                    best_value, best_action = new_value, action

        return best_value, best_action

    def choose_best_action(self, board: Board, players, current_player_index):
        # Find the nearest player to the goal except the current player
        current_player = players[current_player_index]

        nearest_player_index = None
        shortest_distance = float('inf')

        for i, player in enumerate(players):
            if i != current_player_index:
                distance = EvaluationFunction.a_star_path_length(board, player)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_player_index = i

        # Use minimax to determine the best action for the current player against the nearest player
        best_value, best_action = self.minimax(GameState(board, [current_player, players[nearest_player_index]],
                                                         0, False), self.depth,
                                               0)

        return best_action

# import copy
# import logging
# from src.board import Board
# from src.config import Direction, MOVE_DIRECTIONS, PossibleMoves, GRID_SIZE
# from src.player import Player
#
# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#
# class AI_Agent_MinMax:
#
#     def __init__(self, max_depth):
#         self.max_depth = max_depth
#
#     def minimax(self, game_state: (Board, [Player], int, int, bool), depth, alpha, beta):
#         board, players, current_player_index, AI_player_index, game_over = game_state
#
#         logging.debug(f"Minimax call: depth={depth}, alpha={alpha}, beta={beta}, current_player_index={current_player_index}")
#
#         if depth == 0 or game_over:
#             return self.evaluate_game_state((board, players, current_player_index, AI_player_index, game_over))
#
#         if current_player_index == AI_player_index:  # minimizing AI player
#             min_eval = float('inf')
#             for child in self.generate_possible_moves(board, players[current_player_index], players):
#                 new_game_state = self.apply_move(board, child, current_player_index, AI_player_index)
#                 eval = self.minimax(new_game_state, depth - 1, alpha, beta)
#                 min_eval = min(min_eval, eval)
#                 beta = min(beta, eval)
#                 if beta <= alpha:
#                     break
#             return min_eval
#         else:  # maximizing other players
#             max_eval = float('-inf')
#             for child in self.generate_possible_moves(board, players[current_player_index], players):
#                 new_game_state = self.apply_move(board, child, current_player_index, AI_player_index)
#                 eval = self.minimax(new_game_state, depth - 1, alpha, beta)
#                 max_eval = max(max_eval, eval)
#                 alpha = max(alpha, eval)
#                 if beta <= alpha:
#                     break
#             return max_eval
#
#     def evaluate_game_state(self, game_state: (Board, [Player], int, int, bool)):
#         board, players, current_player_index, _, _ = game_state
#         ai_path_length = self.bfs_path_length(board, players[current_player_index])
#         score = ai_path_length
#         return score
#
#     def a_star_path_length(self, board, player):
#         from queue import PriorityQueue
#
#         def heuristic(a, b):
#             return abs(a[0] - b[0]) + abs(a[1] - b[1])
#
#         start = (player.x, player.y)
#         goal_positions = Board.get_goal_positions(player.goal)
#         logging.debug(f"Start: {start}, Goal Positions: {goal_positions}")
#
#         open_set = PriorityQueue()
#         open_set.put((0, start))
#         came_from = {}
#         g_score = {node: float("inf") for node in [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
#         g_score[start] = 0
#         f_score = {node: float("inf") for node in [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
#         f_score[start] = min(heuristic(start, goal) for goal in goal_positions)
#
#         while not open_set.empty():
#             current = open_set.get()[1]
#             logging.debug(f"Current: {current}")
#
#             if current in goal_positions:
#                 total_path = [current]
#                 while current in came_from:
#                     current = came_from[current]
#                     total_path.append(current)
#                 path_length = len(total_path) - 1
#                 logging.debug(f"Path found for player at ({player.x}, {player.y}) with length: {path_length}")
#                 return path_length
#
#             for direction in Direction:
#                 dx, dy = MOVE_DIRECTIONS[direction]
#                 neighbor = (current[0] + dx, current[1] + dy)
#                 if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
#                     if board.is_move_legal(neighbor[0], neighbor[1], [], direction, jump=False):
#                         tentative_g_score = g_score[current] + 1
#                         if tentative_g_score < g_score[neighbor]:
#                             came_from[neighbor] = current
#                             g_score[neighbor] = tentative_g_score
#                             f_score[neighbor] = g_score[neighbor] + min(
#                                 heuristic(neighbor, goal) for goal in goal_positions)
#                             if not any(neighbor == item[1] for item in open_set.queue):
#                                 open_set.put((f_score[neighbor], neighbor))
#                                 logging.debug(f"Neighbor: {neighbor}, g_score: {g_score[neighbor]}, f_score: {f_score[neighbor]}")
#                         else:
#                             logging.debug(f"Skipping neighbor {neighbor} with higher g_score")
#                     else:
#                         logging.debug(f"Move to {neighbor} is illegal")
#
#         logging.debug(f"No path found for player at ({player.x}, {player.y})")
#         return float("inf")
#
#     def generate_possible_moves(self, board, player, players):
#         moves = []
#         # Add pawn movements using Direction enum
#         for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
#             if board.is_move_legal(player.x, player.y, players, direction, jump=False):
#                 moves.append((PossibleMoves.MOVE, player, players, player.x + MOVE_DIRECTIONS[direction][0], player.y + MOVE_DIRECTIONS[direction][1], direction))
#                 logging.debug(f"Generated move: {PossibleMoves.MOVE}, {player.x + MOVE_DIRECTIONS[direction][0]}, {player.y + MOVE_DIRECTIONS[direction][1]}")
#
#         # Add wall placements
#         if player.walls_left == 0:
#             return moves
#         for x in range(GRID_SIZE - 1):
#             for y in range(GRID_SIZE - 1):
#                 for orientation in ['h', 'v']:
#                     if board.can_place_wall(x, y, orientation, players):
#                         moves.append((PossibleMoves.WALL, x, y, orientation, players))
#                         logging.debug(f"Generated wall placement: {PossibleMoves.WALL}, {x}, {y}, {orientation}")
#
#         return moves
#
#     def choose_best_move(self, game_state: (Board, [Player], int, int, bool)):
#         board, players, current_player_index, AI_player_index, _ = copy.deepcopy(game_state)
#         current_player = players[AI_player_index]
#         best_move = None
#         best_score = float('inf')
#         for move in self.generate_possible_moves(board, current_player, players):
#             new_game_state = self.apply_move(board, move, current_player_index, AI_player_index)
#             score = self.minimax(new_game_state, self.max_depth, float('-inf'), float('inf'))
#             if score < best_score:
#                 best_score = score
#                 best_move = move
#         return best_move
#
#     def bfs_path_length(self, board, player):
#         from collections import deque
#
#         goal_positions = Board.get_goal_positions(player.goal)
#         start = (player.x, player.y)
#         queue = deque([(start, 0)])  # (position, path_length)
#         visited = set([start])
#
#         while queue:
#             (x, y), path_length = queue.popleft()
#             if (x, y) in goal_positions:
#                 return path_length  # Return the path length to the goal
#
#             for direction, (dx, dy) in MOVE_DIRECTIONS.items():
#                 new_x, new_y = x + dx, y + dy
#                 if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in visited:
#                     if board.is_move_legal(new_x, new_y, [], direction, jump=False):
#                         queue.append(((new_x, new_y), path_length + 1))
#                         visited.add((new_x, new_y))
#
#         return float("inf")  # No path to the goal was found
#
#     def apply_move(self, board, move, current_player_index, AI_player_index):
#         board = copy.deepcopy(board)
#         result = None
#         game_over = False
#         if move[0] == PossibleMoves.MOVE:
#             player, players, new_x, new_y, direction = copy.deepcopy(move[1]), copy.deepcopy(move[2]), move[3], move[4], move[5]
#             for p in players:
#                 if p.x == new_x and p.y == new_y:
#                     if not board.check_win_condition(player.goal, new_x, new_y):
#                         player.x, player.y = (new_x + MOVE_DIRECTIONS[direction][0],
#                                               new_y + MOVE_DIRECTIONS[direction][1])
#                         break
#             player.x += MOVE_DIRECTIONS[direction][0]
#             player.y += MOVE_DIRECTIONS[direction][1]
#             if board.check_win_condition(player.goal, player.x, player.y):
#                 game_over = True
#             current_player_index = (current_player_index + 1) % len(players)
#             result = (board, players, current_player_index, AI_player_index, game_over)
#         elif move[0] == PossibleMoves.WALL:
#             x, y, orientation, players = move[1], move[2], move[3], move[4]
#             board.set_wall(x, y, orientation)
#             players[current_player_index].walls_left -= 1
#             current_player_index = (current_player_index + 1) % len(players)
#             result = (board, players, current_player_index, AI_player_index, game_over)
#         return result
