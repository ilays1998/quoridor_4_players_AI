from src.Monte_Carlo_Elyashiv import AI_Agent_MonteCarlo_1
from src.ai_game import AI_Game
from src.board import Board
from src.ai_agent_random import AI_Agent_Random
from src.ai_agent_minmax import AI_AgentMinMax
from src.ai_agent_montecarlo import AI_Agent_MonteCarlo
from src.ai_agent_minmax import AI_AgentAlphaBeta
from src.config import *
from src.game_state import GameState
from src.player import Player, PlayerFactory
from src.ai_agent_minmax import EvaluationFunction
import time
from collections import defaultdict
from collections import Counter
from numpy import mean
import random

class NullEvaluationFunction(EvaluationFunction):
    def evaluate(self, state: GameState, other_player_index, AI_player_index):
        return 0

def run_games(players, number_of_games):
    results = []
    game_lengths = []
    turns_lengths = defaultdict(list)
    for _ in range(number_of_games):
        random.shuffle(players)
        game = AI_Game(Board(), players)
        start_time = time.process_time()
        try:
            game.run()
        except TypeError:
            continue
        game_lengths.append(time.process_time() - start_time)
        for player_index, player in enumerate(players):
            if game.players_turns_times[player_index]:
                turns_lengths[player.name].append(mean(game.players_turns_times[player_index]))
        results.append(game.winner.name)

    print(f"Number of games: {number_of_games}")
    print(f"Results (number of wins): {Counter(results)}")
    print(f"Average game length: {mean(game_lengths)}")
    for player_index, player in enumerate(players):
        print(f"{player.name} average turn length: {mean(turns_lengths[player.name])}")
    print()

def stats_1():
    """ alpha-beta with depth 2 against 3 random players """
    print("## alpha-beta with depth 2 against 3 random players ##")
    player_1 = Player(RED, "alpha-beta-1", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_2 = Player(RED, "random-1", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    player_3 = Player(RED, "random-2", direction=Direction.UP,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    player_4 = Player(RED, "random-3", direction=Direction.DOWN,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    players = [player_1, player_2, player_3, player_4]
    run_games(players, 100)

def stats_2():
    """ 2 alpha-betas with depth 2 against 2 alpha-betas depth 1  """
    print("## alpha-beta with depth 2 against 3 alpha-betas depth 1 ##")
    player_1 = Player(RED, "alpha-beta-d1-1", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(1))
    player_2 = Player(RED, "alpha-beta-d2-2", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_3 = Player(RED, "alpha-beta-d2-1", direction=Direction.UP,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_4 = Player(RED, "alpha-beta-d1-2", direction=Direction.DOWN,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(1))
    players = [player_1, player_2, player_3, player_4]
    run_games(players, 50)

def stats_3():
    """ 2-player: random against monte carlo """
    print("#####")
    print("2-player game:")
    print("player 1: monte carlo with 1000 iterations, const 2 and depth 100")
    print("player 2: random")
    print("#####")
    player_1 = Player(RED, "random", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    player_2 = Player(RED, "monte-carlo", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_Agent_MonteCarlo_1(1000, 2, 100))
    players = [player_1, player_2]
    run_games(players, 25)

def stats_4():
    """ 2-player: monte acrlo against minimax """
    print("#####")
    print("2-player game:")
    print("player 1: monte carlo with 1000 iterations, const 2 and depth 100")
    print("player 2: alpha beta depth 1")
    print("#####")
    player_1 = Player(RED, "alpha-beta", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_2 = Player(RED, "monte-carlo", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_Agent_MonteCarlo_1(1000, 2, 100))
    players = [player_1, player_2]
    run_games(players, 5)

def stats_5():
    """ 2-player: monte acrlo against minimax """
    print("#####")
    print("2-player game:")
    print("player 1: monte carlo with 1000 iterations, const 2 and depth 100")
    print("player 2: alpha beta depth 1")
    print("#####")
    player_1 = Player(RED, "alpha-beta", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_2 = Player(RED, "monte-carlo", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_Agent_MonteCarlo_1(10000, 2, 100))
    players = [player_1, player_2]
    run_games(players, 5)


if __name__ == "__main__":
    stats_5()