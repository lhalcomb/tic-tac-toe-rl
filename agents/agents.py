from utils import SYMBOLS

############ Agents #############
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
        return pos - 1
    
class AgentPlayer: 

    """ 
    This class contains the value and policy iteration logic for the tic-tac-toe agent. 

    """
    def __init__(self):
        pass
    
    def get_move(self, env) -> int: 
        return 0