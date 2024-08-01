import abc

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
        ai_distance += state.players[AI_player_index].walls_left

        other_players_distance = 0
        for i, player in enumerate(state.players):
            if i != AI_player_index:
                player_not_ai_distance = EvaluationFunction.a_star_path_length(state.board, player)
                other_players_distance += player_not_ai_distance
                other_players_distance -= state.players[i].walls_left

        # TODO: improve evaluation function
        return ai_distance - other_players_distance


class AI_agent:
    def __init__(self, depth):
        self.depth = depth

    @abc.abstractmethod
    def choose_best_action(self, board: Board, players, current_player_index):
        return


class AI_AgentMinMax(AI_agent):

    def __init__(self, depth):
        super().__init__(depth)

    def minimax(self, state: GameState, depth, player_index, other_players):
        if depth == 0:
            return EvaluationFunction.evaluate(state, player_index), None

        actions = state.generate_possible_moves(state.current_player_index, other_players)
        best_action = None

        if player_index != 0:
            best_value = float('-inf')
            for action in actions:
                successor = state.apply_move(action)
                if successor.game_over:
                    return EvaluationFunction.evaluate(state, player_index), action
                new_value, _ = self.minimax(successor, depth - 1, player_index, other_players)
                if new_value > best_value:
                    best_value, best_action = new_value, action
        else:
            best_value = float('inf')
            for action in actions:
                successor = state.apply_move(action)
                if successor.game_over:
                    return EvaluationFunction.evaluate(state, player_index), action
                new_value, _ = self.minimax(successor, depth - 1, player_index, other_players)
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
                                               0, players)

        return best_action


class AI_AgentAlphaBeta(AI_agent):
    # TODO: Implement alpha-beta pruning this class not work well
    def __init__(self, depth):
        super().__init__(depth)
        self.transposition_table = {}

    def alphabeta(self, state: GameState, depth, alpha, beta, player_index, other_players):
        state_key = state.hash()  # Assuming GameState has a hash method
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        if depth == 0 or state.game_over:
            value = EvaluationFunction.evaluate(state, player_index)
            self.transposition_table[state_key] = (value, None)
            return value, None

        actions = state.generate_possible_moves(state.current_player_index, other_players)
        best_action = None

        if player_index != 0:  # Maximizing player
            best_value = float('-inf')
            for action in actions:
                successor = state.apply_move(action)
                new_value, _ = self.alphabeta(successor, depth - 1, alpha, beta, player_index, other_players)
                if new_value > best_value:
                    best_value, best_action = new_value, action
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    print(f"Pruned at depth {depth} with alpha {alpha} and beta {beta}")
                    break
        else:  # Minimizing player
            best_value = float('inf')
            for action in actions:
                successor = state.apply_move(action)
                new_value, _ = self.alphabeta(successor, depth - 1, alpha, beta, player_index, other_players)
                if new_value < best_value:
                    best_value, best_action = new_value, action
                beta = min(beta, best_value)
                if alpha >= beta:
                    print(f"Pruned at depth {depth} with alpha {alpha} and beta {beta}")
                    break

        self.transposition_table[state_key] = (best_value, best_action)
        return best_value, best_action

    def choose_best_action(self, board: Board, players, current_player_index):
        current_player = players[current_player_index]

        nearest_player_index = None
        shortest_distance = float('inf')

        for i, player in enumerate(players):
            if i != current_player_index:
                distance = EvaluationFunction.a_star_path_length(board, player)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_player_index = i

        best_value, best_action = self.alphabeta(
            GameState(board, [current_player, players[nearest_player_index]], 0, False),
            self.depth, float('-inf'), float('inf'), 0, players)

        return best_action

