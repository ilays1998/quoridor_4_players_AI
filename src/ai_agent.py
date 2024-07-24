from src.config import Direction
from src.game import Game


class AI_Agent:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or game_state.is_terminal():
            return self.evaluate_game_state(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            for child in self.generate_possible_moves(game_state):
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.generate_possible_moves(game_state):
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_game_state(self, game_state):
        # TODO: the evaluation function should be improved
        #  as the short path for AI and longer path for the best opponent
        ai_path_length = self.a_star_path_length(game_state, self)
        opponent_path_lengths = [self.a_star_path_length(game_state, opponent) for opponent in game_state.opponents]
        score = ai_path_length - sum(
            opponent_path_lengths)  # Favor states with shorter path for AI and longer paths for opponents
        return score

    def a_star_path_length(self, board, player):
        from queue import PriorityQueue

        def heuristic(a, b):
            # Manhattan distance on a square grid
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (player.x, player.y)
        goal_positions = board.get_goal_positions(player.goal)

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {node: float("inf") for node in
                   [(x, y) for x in range(board.GRID_SIZE) for y in range(board.GRID_SIZE)]}
        g_score[start] = 0
        f_score = {node: float("inf") for node in
                   [(x, y) for x in range(board.GRID_SIZE) for y in range(board.GRID_SIZE)]}
        f_score[start] = min(heuristic(start, goal) for goal in goal_positions)

        while not open_set.empty():
            current = open_set.get()[1]

            if current in goal_positions:
                total_path = [current]
                while current in came_from:
                    current = came_from[current]
                    total_path.append(current)
                return len(total_path) - 1

            for direction in Direction:
                dx, dy = direction.value
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < board.GRID_SIZE and 0 <= neighbor[1] < board.GRID_SIZE:
                    if board.is_move_legal(neighbor[0], neighbor[1], [player], direction):
                        tentative_g_score = g_score[current] + 1
                        if tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = g_score[neighbor] + min(
                                heuristic(neighbor, goal) for goal in goal_positions)
                            if not any(neighbor == item[1] for item in open_set.queue):
                                open_set.put((f_score[neighbor], neighbor))

        return float("inf")

    def generate_possible_moves(self, board, player):
        # TODO: return Game objects instead of moves
        moves = []
        # Add pawn movements using Direction enum
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            if board.is_move_legal(player.x, player.y, [player], direction):
                moves.append(('MOVE', direction.name))
        # Add wall placements
        for x in range(board.GRID_SIZE):
            for y in range(board.GRID_SIZE):
                for orientation in ['h', 'v']:
                    if board.can_place_wall(x, y, orientation, [player]):
                        moves.append(('WALL', x, y, orientation))
        return moves

    def choose_best_move(self, game_state: Game, maximizing_player=True):
        # TODO Game parameter need to be a deep copy of the game state
        best_move = None
        best_score = float('-inf') if maximizing_player else float('inf')
        for move in self.generate_possible_moves(game_state.board, game_state.players[game_state.current_player_index]):
            new_game_state = game_state.apply_move(move)
            score = self.minimax(new_game_state, self.max_depth, float('-inf'), float('inf'), not maximizing_player)
            if maximizing_player and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing_player and score < best_score:
                best_score = score
                best_move = move
        return best_move
