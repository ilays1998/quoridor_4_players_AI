import copy
import math
import random
from src.board import Board
from src.config import Direction, MOVE_DIRECTIONS, PossibleMoves, GRID_SIZE
from src.game_state import GameState
from src.ai_agent_minmax import EvaluationFunction


class AI_Agent_MonteCarlo():

    def __init__(self, max_iterations, exploration_constant):
        self.player_index = None
        self.max_iterations = max_iterations
        self.exploration_constant = exploration_constant

    def choose_best_action(self, board: Board, players, current_player_index):
        self.player_index = current_player_index
        game_state = GameState(board, players, current_player_index, False)
        return self.mcts(game_state)

    def mcts(self, game_state: GameState):
        root = Node(game_state)
        for _ in range(self.max_iterations):
            node = self.select(root)
            reward = self.simulate(node)
            self.backpropagate(node, reward)
        return self.best_child(root).move

    def select(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                #todo check if we even want to return the best child in that case
                # or  just move to another ranch
                node = self.best_uct_child(node)
        return node

    def expand(self, node):
        move = node.untried_moves.pop()
        next_state = node.state.apply_move(move)
        child_node = Node(next_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node

    def simulate(self, node):
        game_state = node.state
        def simulate_policy(moves):
            return random.choice(moves)
            best_move = None
            best_score = float("-inf")

            random.shuffle(moves)
            for move in moves:
                current_player_distance = EvaluationFunction.a_star_path_length(board, players[current_player_index])
                for player_index, player in enumerate(players):
                    if player_index != current_player_index:
                        other_player_distance = EvaluationFunction.a_star_path_length(board, players[player_index])
                        score = other_player_distance - current_player_distance
                        if score > best_score:
                            best_score = score
                            best_move = move
                # score = -current_player_distance
                # if score > best_score:
                #     best_score = score
                #     best_move = move
            return best_move

        iter = 0
        while not game_state.game_over:
            # print(iter)
            iter += 1
            board = game_state.board
            players = game_state.players
            current_player_index = game_state.current_player_index

            # print(game_state)
            possible_moves = game_state.generate_possible_moves(current_player_index, players)
            if possible_moves is None or not possible_moves:
                print("game is over: " + game_state.game_over)
                print(game_state)
            move = simulate_policy(possible_moves)
            # print(move)
            game_state = game_state.apply_move(move)
            # current_player_index = (current_player_index + 1) % len(players)
        # return self.evaluate_game_state(game_state)
        return self.reward(game_state)

    def reward(self, game_state):
        return game_state.get_winner() == self.player_index  # return 0 if other won 1 if we

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def best_uct_child(self, node):
        best_score = float('-inf')
        best_child = None
        for child in node.children:
            exploit = child.reward / child.visits
            # if child.visits == 0:
            #     return child
            explore = math.sqrt(math.log(node.visits) / child.visits)
            score = exploit + self.exploration_constant * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def best_child(self, node):
        """
        Returns the child with the highest average reward
        """
        best_child = None
        best_score = float("-inf")
        assert (len(node.children) != 0)
        for child in node.children:
            score = child.visits
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    # def apply_move(self, game_state: GameState, move):
    #     return game_state.apply_move(move)
    # board, players, current_player_index, AI_player_index, game_over = game_state
    # board = copy.deepcopy(board)
    # if move[0] == PossibleMoves.MOVE:
    #     player, players, new_x, new_y, direction = copy.deepcopy(move[1]), copy.deepcopy(move[2]), move[3], move[4], \
    #     move[5]
    #     for p in players:
    #         if p.x == new_x and p.y == new_y:
    #             if not board.check_win_condition(player.goal, new_x, new_y):
    #                 player.x, player.y = (new_x + MOVE_DIRECTIONS[direction][0],
    #                                       new_y + MOVE_DIRECTIONS[direction][1])
    #                 break
    #     player.x += MOVE_DIRECTIONS[direction][0]
    #     player.y += MOVE_DIRECTIONS[direction][1]
    #     if board.check_win_condition(player.goal, player.x, player.y):
    #         game_over = True
    #     current_player_index = (current_player_index + 1) % len(players)
    # elif move[0] == PossibleMoves.WALL:
    #     x, y, orientation, players = move[1], move[2], move[3], move[4]
    #     board.set_wall(x, y, orientation)
    #     players[current_player_index].walls_left -= 1
    #     current_player_index = (current_player_index + 1) % len(players)
    # return (board, players, current_player_index, AI_player_index, game_over)

    # replaced by reward
    # def evaluate_game_state(self, game_state):
    #     board, players, current_player_index, _, _ = game_state
    #     ai_path_length = self.a_star_path_length(board, players[current_player_index])
    #     score = ai_path_length
    #     return score

    # def generate_possible_moves(self, board, player, players):
    #     return
    # moves = []
    # for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
    #     if board.is_move_legal(player.x, player.y, players, direction, player, jump=False):
    #         moves.append((PossibleMoves.MOVE, player, players, player.x + MOVE_DIRECTIONS[direction][0],
    #                       player.y + MOVE_DIRECTIONS[direction][1], direction))
    # if player.walls_left > 0:
    #     for x in range(GRID_SIZE - 1):
    #         for y in range(GRID_SIZE - 1):
    #             for orientation in ['h', 'v']:
    #                 if board.can_place_wall(x, y, orientation, players):
    #                     moves.append((PossibleMoves.WALL, x, y, orientation, players))
    # return moves

    # def a_star_path_length(self, board, player):
    #     from queue import PriorityQueue
    #
    #     def heuristic(a, b):
    #         return abs(a[0] - b[0]) + abs(a[1] - b[1])
    #
    #     start = (player.x, player.y)
    #     goal_positions = Board.get_goal_positions(player.goal)
    #
    #     open_set = PriorityQueue()
    #     open_set.put((0, start))
    #     came_from = {}
    #     g_score = {node: float("inf") for node in [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
    #     g_score[start] = 0
    #     f_score = {node: float("inf") for node in [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]}
    #     f_score[start] = min(heuristic(start, goal) for goal in goal_positions)
    #
    #     while not open_set.empty():
    #         current = open_set.get()[1]
    #
    #         if current in goal_positions:
    #             total_path = [current]
    #             while current in came_from:
    #                 current = came_from[current]
    #                 total_path.append(current)
    #             return len(total_path) - 1
    #
    #         for direction in Direction:
    #             dx, dy = MOVE_DIRECTIONS[direction]
    #             neighbor = (current[0] + dx, current[1] + dy)
    #             if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
    #                 if board.is_move_legal(neighbor[0], neighbor[1], [], direction, player, jump=False):
    #                     tentative_g_score = g_score[current] + 1
    #                     if tentative_g_score < g_score[neighbor]:
    #                         came_from[neighbor] = current
    #                         g_score[neighbor] = tentative_g_score
    #                         f_score[neighbor] = g_score[neighbor] + min(
    #                             heuristic(neighbor, goal) for goal in goal_positions)
    #                         if not any(neighbor == item[1] for item in open_set.queue):
    #                             open_set.put((f_score[neighbor], neighbor))
    #
    #     return float("inf")


class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = state.generate_possible_moves(state.current_player_index, state.players)
        self.visits = 0
        self.reward = 0

    def is_terminal(self):
        return self.state.game_over

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
