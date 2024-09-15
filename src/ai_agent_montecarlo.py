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
            # if i % 10 == 0: print(i)
            node = self.select(root)
            reward = self.simulate(node)
            self.backpropagate(reward, node)
        # print(self.best_uct_child(root).move)
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