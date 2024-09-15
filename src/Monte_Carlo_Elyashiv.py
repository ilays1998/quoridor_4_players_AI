# # import math
# # import random
# # from collections import defaultdict
# #
# # from src.board import Board
# # from src.config import Direction, MOVE_DIRECTIONS, PossibleMoves, GRID_SIZE
# # from src.game_state import GameState
# # from src.ai_agent_minmax import EvaluationFunction
# #
# # PUNISH_ARG = 2.0
# # class AI_Agent_MonteCarlo_1():
# #
# #     def __init__(self, max_iterations, exploration_constant, max_simulation_iter=float("inf")):
# #         self.player_index = None
# #         self.max_iterations = max_iterations
# #         self.exploration_constant = exploration_constant
# #         self.max_simulation_iter = max_simulation_iter
# #
# #     def choose_best_action(self, board: Board, players, current_player_index):
# #         self.player_index = current_player_index
# #         game_state = GameState(board, players, current_player_index, game_over=False)
# #         return self.mcts(game_state)
# #
# #     def mcts(self, game_state: GameState):
# #         root = Node(game_state)
# #         for _ in range(self.max_iterations):
# #             print(f"iteration number:", _)
# #             node = self.select(root)
# #             reward = self.simulate(node)
# #             self.backpropagate(node, reward)
# #         return self.best_child(root).move
# #
# #     def select(self, node):
# #         while not node.is_terminal():
# #             if not node.is_fully_expanded():
# #                 return self.expand(node)
# #             else:
# #                 node = self.best_uct_child(node)
# #         return node
# #
# #     def expand(self, node):
# #         move = node.untried_moves.pop()
# #         next_state = node.state.apply_move(move)
# #         child_node = Node(next_state, parent=node, move=move)
# #         node.children.append(child_node)
# #         return child_node
# #
# #     from collections import defaultdict
# #
# #     def simulate_best_turn(self, possible_moves, game_state: GameState):
# #         players_init_shortest_path = [EvaluationFunction.a_star_path_length(game_state.board, player)
# #                                       for player in game_state.players]
# #
# #         walls_h = defaultdict(lambda: defaultdict(int))
# #         walls_v = defaultdict(lambda: defaultdict(int))
# #         directions = dict()
# #
# #         for move in possible_moves:
# #             sum_added_to_players = 0
# #             new_state = game_state.apply_move(move)
# #
# #             for i in range(len(game_state.players)):
# #                 new_shortest = EvaluationFunction.a_star_path_length(new_state.board, new_state.players[i])
# #                 if i == self.player_index:
# #                     # Punishment for adding length to ourselves
# #                     sum_added_to_players -= (players_init_shortest_path[i] - new_shortest)
# #                 else:
# #                     sum_added_to_players += (players_init_shortest_path[i] - new_shortest)
# #
# #             if move[0] == PossibleMoves.WALL:
# #                 # Horizontal vs Vertical wall placement
# #                 if move[3] == "h":
# #                     walls_h[move[1]][move[2]] = sum_added_to_players
# #                 else:
# #                     walls_v[move[1]][move[2]] = sum_added_to_players
# #             else:
# #                 directions[move] = sum_added_to_players
# #
# #         # Punishments for horizontal walls
# #         for wall_x in walls_h.keys():
# #             for wall_y in walls_h[wall_x].keys():
# #                 if walls_v[wall_x].get(wall_y):
# #                     walls_h[wall_x][wall_y] += (walls_v[wall_x][wall_y] / PUNISH_ARG)
# #                 if wall_x > 0 and walls_h[wall_x - 1].get(wall_y):
# #                     walls_h[wall_x][wall_y] += (walls_h[wall_x - 1][wall_y] / PUNISH_ARG)
# #                 if wall_x < GRID_SIZE - 2 and walls_h[wall_x + 1].get(wall_y):
# #                     walls_h[wall_x][wall_y] += (walls_h[wall_x + 1][wall_y] / PUNISH_ARG)
# #
# #         # Punishments for vertical walls
# #         for wall_x in walls_v.keys():
# #             for wall_y in walls_v[wall_x].keys():
# #                 if walls_h[wall_x].get(wall_y):
# #                     walls_v[wall_x][wall_y] += (walls_h[wall_x][wall_y] / PUNISH_ARG)
# #                 if wall_y > 0 and walls_v[wall_x].get(wall_y - 1):
# #                     walls_v[wall_x][wall_y] += (walls_v[wall_x][wall_y - 1] / PUNISH_ARG)
# #                 if wall_y < GRID_SIZE - 2 and walls_v[wall_x].get(wall_y + 1):
# #                     walls_v[wall_x][wall_y] += (walls_v[wall_x][wall_y + 1] / PUNISH_ARG)
# #
# #         # Get the best values and moves
# #         best_wall_v = max(([wall_x, wall_y] for wall_x in walls_v for wall_y in walls_v[wall_x]),
# #                           key=lambda x: walls_v[x[0]][x[1]], default=None)
# #         best_wall_h = max(([wall_x, wall_y] for wall_x in walls_h for wall_y in walls_h[wall_x]),
# #                           key=lambda x: walls_h[x[0]][x[1]], default=None)
# #         best_direction = max(directions, key=lambda x: directions[x], default=None)
# #
# #         best_wall_v_value = walls_v[best_wall_v[0]][best_wall_v[1]] if best_wall_v else float('-inf')
# #         best_wall_h_value = walls_h[best_wall_h[0]][best_wall_h[1]] if best_wall_h else float('-inf')
# #         best_direction_value = directions[best_direction] if best_direction else float('-inf')
# #
# #         # Compare the maximum values and choose the best move
# #         if best_wall_h_value >= best_wall_v_value and best_wall_h_value >= best_direction_value:
# #             return PossibleMoves.WALL, best_wall_h[0], best_wall_h[1], "h"
# #         elif best_wall_v_value >= best_wall_h_value and best_wall_v_value >= best_direction_value:
# #             return PossibleMoves.WALL, best_wall_v[0], best_wall_v[1], "v"
# #         else:
# #             return best_direction
# #
# #     def simulate_best_turn1(self, possible_moves, game_state: GameState):
# #         players_init_shortest_path = [EvaluationFunction.a_star_path_length(game_state.board,player)
# #                                       for player in game_state.players]
# #         walls_h = dict()
# #         walls_v = dict()
# #         directions = dict(dict())
# #         for move in possible_moves:
# #             sum_added_to_players = 0
# #             new_state = game_state.apply_move(move)
# #             for i in range(len(game_state.players)):
# #                 new_shortest = EvaluationFunction.a_star_path_length(new_state.board, new_state.players[i])
# #                 if i == self.player_index:
# #                     #if we added length to ourselves its a punishment
# #                     sum_added_to_players -= (players_init_shortest_path[i]-new_shortest)
# #                 else:
# #                     sum_added_to_players += (players_init_shortest_path[i]-new_shortest)
# #
# #             if move[0] == PossibleMoves.WALL:
# #                 #check if it blocks players from making a move that hurts me
# #                 if move[3] == "h":
# #                     walls_h[move[1]][move[2]] = sum_added_to_players
# #                 else:
# #                     walls_v[move[1]][move[2]] = sum_added_to_players
# #             else:
# #                 directions[move] = sum_added_to_players
# #         # punishments:
# #         for wall_x in walls_h.keys():
# #             for wall_y in walls_h.keys():
# #                 # horizontal:
# #                 if walls_v[wall_x][wall_y]:
# #                     walls_h[wall_x][wall_y] += ((walls_v[wall_x][wall_y]) / PUNISH_ARG)
# #                 if wall_x > 0 and walls_h[wall_x - 1][wall_y]:
# #                     walls_h[wall_x][wall_y] += ((walls_h[wall_x - 1][wall_y]) / PUNISH_ARG)
# #                 if wall_x < GRID_SIZE - 2 and walls_h[wall_x + 1][wall_y]:
# #                     walls_h[wall_x][wall_y] += ((walls_h[wall_x - 1][wall_y]) / PUNISH_ARG)
# #         for wall_x in walls_v.keys():
# #             for wall_y in walls_v.keys():
# #                 # vertical:
# #                 if walls_h[wall_x][wall_y]:
# #                     walls_v[wall_x][wall_y] += ((walls_h[wall_x][wall_y]) / PUNISH_ARG)
# #                 if wall_y > 0 and walls_v[wall_x][wall_y-1]:
# #                     walls_v[wall_x][wall_y] += ((walls_v[wall_x][wall_y-1]) / PUNISH_ARG)
# #                 if wall_y < GRID_SIZE - 2 and walls_v[wall_x][wall_y+1]:
# #                     walls_v[wall_x][wall_y] += ((walls_v[wall_x][wall_y+1]) / PUNISH_ARG)
# #         max_wall_v = max(walls_v.values())
# #         max_wall_h = max(walls_h.values())
# #         max_direction = max(directions.values())
# #
# #     def simulate(self, node):
# #         game_state = node.state
# #
# #         simulation_iter = 0
# #         while not game_state.game_over and simulation_iter < self.max_simulation_iter:
# #             simulation_iter += 1
# #             board = game_state.board
# #             players = game_state.players
# #             current_player_index = game_state.current_player_index
# #
# #             possible_moves = game_state.generate_possible_moves(current_player_index, players)
# #             if possible_moves is None or not possible_moves:
# #                 print("game is over: " + game_state.game_over)
# #                 print(game_state)
# #             move = self.simulate_best_turn(possible_moves, game_state)
# #             # print(move)
# #             game_state = game_state.apply_move(move)
# #
# #         return self.reward(game_state)
# #
# #     def reward(self, game_state):
# #         if game_state.game_over:
# #             if game_state.get_winner() == self.player_index:
# #                 return 1000
# #             else:
# #                 return -1000
# #
# #         return - EvaluationFunction.a_star_path_length(game_state.board, game_state.players[self.player_index])
# #
# #     def backpropagate(self, node, reward):
# #         while node is not None:
# #             node.visits += 1
# #             node.reward += reward
# #             node = node.parent
# #
# #     def best_uct_child(self, node):
# #         best_score = float('-inf')
# #         best_child = None
# #         for child in node.children:
# #             exploit = child.reward / child.visits
# #             explore = math.sqrt(math.log(node.visits) / child.visits)
# #             score = exploit + self.exploration_constant * explore
# #             if score > best_score:
# #                 best_score = score
# #                 best_child = child
# #         return best_child
# #
# #     def best_child(self, node):
# #         """
# #         Returns the child with the highest average reward
# #         """
# #         best_child = None
# #         best_score = float("-inf")
# #         assert (len(node.children) != 0)
# #         for child in node.children:
# #             score = child.visits
# #             if score > best_score:
# #                 best_score = score
# #                 best_child = child
# #         return best_child
# import math
# import random
# import concurrent.futures
#
# from src.ai_agent_minmax import EvaluationFunction
# from src.config import PossibleMoves
# from src.game_state import GameState
#
import math
import random

from src.ai_agent_minmax import EvaluationFunction
from src.board import Board
from src.config import PossibleMoves, Direction
from src.game_state import GameState


class Node:
    def __init__(self, state: GameState, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.untried_moves = state.generate_probable_moves(state.current_player_index, state.players)
        self.visits = 0
        self.reward = 0

    def is_terminal(self):
        return self.state.game_over

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0


from src.board import Board
from src.game_state import GameState

WIN_REWARD = 1000
LOSE_REWARD = -1000


class AI_Agent_MonteCarlo_1():

    def __init__(self, max_iterations, exploration_constant, max_simulation_iter=float("inf")):
        self.player_index = None
        self.max_iterations = max_iterations
        self.exploration_constant = exploration_constant
        self.max_simulation_iter = max_simulation_iter

    def choose_best_action(self, board: Board, players, current_player_index):
        self.player_index = current_player_index
        return self.mcts(board, players, current_player_index)

    def opposite(self, direction):
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
        if direction == Direction.RIGHT:
            return Direction.LEFT
        if direction == Direction.LEFT:
            return Direction.RIGHT


    def cost(self, state, move):
        if move[0] == PossibleMoves.MOVE:
            if move[3] == state.players[state.current_player_index].goal:
                return 36
            if move[3] == self.opposite(state.players[state.current_player_index].goal):
                return 2
            else:
                return 16
        else:
            return 1


    def mcts(self, board, players, current_player_index):
        state = GameState(board, players, current_player_index, game_over=False)
        root = Node(state, None, None)
        for i in range(self.max_iterations):
            if i % 10 == 0: print(i)
            node = self.select(root)
            reward = self.simulate(node)
            self.backpropagate(reward, node)
        print(self.best_uct_child(root).move)
        return self.best_uct_child(root).move

    def select(self, root: Node):
        node = root
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = self.best_uct_child(node)
        return node

    def expand(self, node: Node):
        move = node.untried_moves.pop()
        next_state = node.state.apply_move(move)
        child_node = Node(next_state, parent=node, move=move)
        node.children.append(child_node)
        return child_node

    def reward(self, state: GameState):
        if state.game_over:
            if state.get_winner() == self.player_index:
                return WIN_REWARD - state.players[self.player_index].walls_left
            else:
                return LOSE_REWARD - state.players[self.player_index].walls_left
        return self.evaluate(state) - state.players[self.player_index].walls_left

    # def expand(self, node: Node):
    #     move = node.untried_moves.pop()
    #     next_state = node.state.apply_move(move)
    #     child_node = Node(next_state, parent=node, move=move)
    #     node.children.append(child_node)
    #
    #     # Run the simulation for this new child node using multiprocessing
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         future = executor.submit(self.simulate, child_node)
    #         simulation_result = future.result()
    #
    #     self.backpropagate(simulation_result, child_node)
    #     return child_node

    def uct(self, node):
        exploit = node.reward / node.visits
        explore = math.sqrt(math.log(node.visits) / node.visits)
        return exploit + self.exploration_constant * explore

    def best_uct_child(self, node):
        assert len(node.children) != 0
        return max(node.children, key=lambda child: self.uct(child))

    def choose_well(self,state, moves):
        # return random.choice(moves)
        # choose non uniformly:
        cummultive_reward = 0
        for move in moves:
            cummultive_reward += self.cost(state, move)
        pick = random.randint(0, cummultive_reward)
        for move in moves:
            cost = self.cost(state, move)
            if pick <= cost:
                return move
            pick -= cost
        raise ValueError("not suppose to happen", pick, cummultive_reward, moves[-1])

    def simulate(self, node: Node):
        state = GameState(node.state.board, node.state.players, node.state.current_player_index, game_over=False)
        i = 0
        while (not state.game_over) and i < self.max_simulation_iter:
            moves = state.generate_probable_moves(state.current_player_index, state.players)
            if len(moves) == 0:
                return self.reward(state)
            move = self.choose_well(state, moves)
            state = state.apply_move_no_cpy(move)
            i += 1
        return self.reward(state)

    def evaluate(self, state):
        # other_player_length = 0
        # for i in range(len(state.players)):
        #     if i == self.player_index:
        #         player_length = (EvaluationFunction.a_star_path_length
        #                          (state.board, state.players[self.player_index]))
        #     else:
        #         other_player_length += (EvaluationFunction.a_star_path_length
        #                          (state.board, state.players[i]))
        # return -player_length+((other_player_length)/(len(state.players)-1))
        return -EvaluationFunction.a_star_path_length(state.board, state.players[self.player_index])

    def backpropagate(self, reward, node):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent
# import math
# import random
#
#
# class AI_Agent_MonteCarlo_1:
#     def __init__(self, max_iterations, exploration_constant, max_simulation_iter=float("inf")):
#         self.max_iterations = max_iterations
#         self.exploration_constant = exploration_constant
#         self.max_simulation_iter = max_simulation_iter
#
#     def choose_best_action(self, board: Board, players, current_player_index):
#         self.player_index = current_player_index
#         return self.mcts(GameState(board, players, current_player_index, game_over=False))
#
#     def mcts(self, game_state):
#         root = Node(game_state)
#         for _ in range(self.max_iterations):
#             node = self.select(root)
#             reward = self.simulate(node)
#             self.backpropagate(node, reward)
#         return self.best_uct_child(root).move
#
#     def select(self, node):
#         while not node.is_terminal():
#             if not node.is_fully_expanded():
#                 return self.expand(node)
#             node = self.best_uct_child(node)
#         return node
#
#     def expand(self, node):
#         move = node.untried_moves.pop()
#         next_state = node.state.apply_move(move)
#         child_node = Node(next_state, parent=node, move=move)
#         node.children.append(child_node)
#         return child_node
#
#     def simulate(self, node):
#         game_state = node.state
#         simulation_iter = 0
#         while not game_state.game_over and simulation_iter < self.max_simulation_iter:
#             simulation_iter += 1
#             possible_moves = game_state.generate_possible_moves(game_state.current_player_index, game_state.players)
#             move = self.choose_well(possible_moves)
#             game_state = game_state.apply_move(move)
#         return self.reward(game_state)
#
#     def choose_well(self, moves):
#         total_reward = sum(move[1] for move in moves)
#         pick = random.uniform(0, total_reward)
#         current = 0
#         for move in moves:
#             current += move[1]
#             if current >= pick:
#                 return move
#         return moves[-1]
#
#     def backpropagate(self, node, reward):
#         while node is not None:
#             node.visits += 1
#             node.reward += reward
#             node = node.parent
#
#     def best_uct_child(self, node):
#         best_score = float('-inf')
#         best_child = None
#         for child in node.children:
#             score = self.uct(child)
#             if score > best_score:
#                 best_score = score
#                 best_child = child
#         return best_child
#
#     def uct(self, node):
#         exploit = node.reward / node.visits
#         explore = math.sqrt(math.log(node.parent.visits) / node.visits)
#         return exploit + self.exploration_constant * explore
#
#     def reward(self, state: GameState, WIN_REWARD=None, LOSE_REWARD=None):
#         if state.game_over:
#             if state.get_winner() == self.player_index:
#                 return WIN_REWARD -state.players[self.player_index].walls_left
#             else:
#                 return LOSE_REWARD-state.players[self.player_index].walls_left
#         return self.evaluate(state) -state.players[self.player_index].walls_left
#
#     def evaluate(self, state):
#             # other_player_length = 0
#             # for i in range(len(state.players)):
#             #     if i == self.player_index:
#             #         player_length = (EvaluationFunction.a_star_path_length
#             #                          (state.board, state.players[self.player_index]))
#             #     else:
#             #         other_player_length += (EvaluationFunction.a_star_path_length
#             #                          (state.board, state.players[i]))
#             # return -player_length+((other_player_length)/(len(state.players)-1))
#         return -EvaluationFunction.a_star_path_length(state.board, state.players[self.player_index])
