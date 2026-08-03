from utils import SYMBOLS, Player

############ Agents Controller Classes #############

"""

These control the different agent player logic across the rl algorithms and gameplay.

"""
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
    def __init__(self): 
        pass

    def get_move(self, env) -> int:
        return 0

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