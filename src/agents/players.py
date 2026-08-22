from src.agents.minimax import MiniMax
from src.agents.mcts import MCTS
from src.utils.utility import SYMBOLS, Player

import random

############ Agents Controller Classes ############
#These control the different agent player logic across the rl algorithms and gameplay.

class HumanPlayer:
    def get_move(self, env) -> int:
        while True:
            try:
                pos = int(input(f"{SYMBOLS[env.turn]} turn - place piece: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            return pos - 1

class RandomPlayer:  # placeholder 
    def get_move(self, env) -> int:
        import random
        pos = random.choice(env.valid_moves()) 
        print(f"{SYMBOLS[env.turn]} turn - place piece:  ", pos)
        return pos

class MiniMaxPlayer:
    def __init__(self, agent): 
        self.agent = agent
        self.minimax = MiniMax(agent)

    def get_move(self, env) -> int:
        state = (env.cross, env.nought, SYMBOLS[env.turn])
        action_mask = self.minimax.get_best_action(state)

        return action_mask.bit_length() - 1 if action_mask != None else 0b000000000

class PolicyPlayer:
    def __init__(self, policy: dict, agent: Player):
        self.policy = policy
        self.agent = agent

    def get_move(self, env) -> int:
        state = (env.cross, env.nought, SYMBOLS[env.turn])
        action_mask = self.policy[state]
        pos = action_mask.bit_length() - 1
        print(pos)
        assert pos in env.valid_moves(), (
            f"illegal move: state={state}, action_mask={action_mask}, pos={pos}, "
            f"valid={env.valid_moves()}"
        )
        return pos

class MCTSPlayer:
    def __init__(self, agent: Player):
        self.agent = agent
        self.mcts = MCTS(self.agent)

    def get_move(self, env) -> int:
        state = (env.cross, env.nought, SYMBOLS[env.turn])
        action_mask = self.mcts.search(state)
        return action_mask.bit_length() - 1 if action_mask != None else 0b000000000

class QLearningPlayer:
    def __init__(self, q_table: dict, agent: Player):
        self.q_table = q_table
        self.agent = agent

    def get_move(self, env) -> int:
        state = (env.cross, env.nought, SYMBOLS[env.turn])
        q_values = self.q_table.get(state)

        if not q_values:
            # never visited this state during training — fall back to a
            # legal random move rather than crashing
            action_mask = random.choice(env.valid_moves and [1 << p for p in env.valid_moves()])
        else:
            action_mask = max(q_values, key=q_values.get)

        pos = action_mask.bit_length() - 1
        assert pos in env.valid_moves(), (
            f"illegal move: state={state}, action_mask={action_mask}, pos={pos}, "
            f"valid={env.valid_moves()}"
        )
        return pos
