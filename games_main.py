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
from numpy import mean

class NullEvaluationFunction(EvaluationFunction):
    def evaluate(self, state: GameState, other_player_index, AI_player_index):
        return 0

if __name__ == "__main__":
    player_1 = Player(RED, "1", direction=Direction.LEFT,
                      player_is_AI=True, ai_agent=AI_AgentAlphaBeta(2))
    player_2 = Player(RED, "2", direction=Direction.RIGHT,
                      player_is_AI=True, ai_agent=AI_Agent_MonteCarlo(10000, 2, max_simulation_iter=1))
    player_3 = Player(RED, "3", direction=Direction.UP,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    player_4 = Player(RED, "4", direction=Direction.DOWN,
                      player_is_AI=True, ai_agent=AI_Agent_Random())
    players = [player_1, player_2]
    results = []
    durations = []
    print("starting player 1: "+str(player_1.get_position()))
    print("starting player 2: "+str(player_2.get_position()))
    for i in range(10):
        game = AI_Game(Board(), players)
        start_time = time.process_time()
        game.run()
        durations.append(time.process_time() - start_time)
        results.append(game.winner.name)
    from collections import Counter
    print(Counter(results))
    print(mean(durations))