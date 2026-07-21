
"""
Implementation of RL-Agents playing Tic-Tac-Toe 


RL algorithms utilized: 
    - Policy & Value Iteration
    - Q-Learning
    - MCTS

Sources: 
    - https://github.com/bsamseth/tic-tac-toe/blob/master/tictactoe.py
    - Russell, S. J., and Peter Norvig. Artificial Intelligence: A Modern Approach. 4th ed., Pearson, 2020.
    - Sutton, Richard S., and Andrew G. Barto. Reinforcement Learning: An Introduction. 2nd ed., The MIT Press, 2018.
    - https://huggingface.co/learn/deep-rl-course

"""
from enum import Enum
from collections import deque 

########## ENUMS/STRUCTS ##########
class Player(Enum):
    EMPTY = 0
    CROSS = 1
    NOUGHT = 2

# I like to instantiate all of my constants at the top. B/c once upon a time I learned C.
############ CONSTANTS ############
SIZE = 3
# Winning patterns encoded in bit patterns.
# E.g. three in a row in the top row is
#   448 = 0b111000000
WINNING_PATTERNS = [
        448, 56, 7,   # Rows
        292, 146, 73, # Columns
        273, 84       # Diagonals
]
FULL_BOARD = 0b111111111

SYMBOLS = {Player.EMPTY: ".", Player.CROSS: "X", Player.NOUGHT: "O"}

############ Helper Functions ############
def bits_of(mask: int):
    while mask:
        low = mask & -mask
        yield low     # pause here, hand back `low`, remember where we are
        mask = mask ^ low   # resumes here on the *next* call

class Environment:
    def __init__(self, player_x, player_o):
        self.cross: int = 0
        self.nought: int = 0
        self.bitboards = [self.cross, self.nought]
        self.turn = Player.CROSS
        self.grid = [Player.EMPTY] * (SIZE * SIZE)

        self.players = {
            Player.CROSS: player_x,
            Player.NOUGHT: player_o,
        }
        

    def __str__(self) -> str:
        return self.render(self.cross, self.nought)

    @property #allows me to do Environment.occupied instead of Environment.occupied() or self.occupied instead of making another attribute
    def occupied(self) -> int:
        return self.cross | self.nought
    
    def valid_moves(self) -> list[int]:
        # return all the valid moves from the current ones occupied
        empty = ~self.occupied & 0b111111111
        return [i for i in range(SIZE ** 2) if empty & (1 << i)]
    
    def place_piece(self, pos: int):

        bit = 1 << pos
        if self.occupied & bit: 
            raise ValueError("There is already a placement here, choose elsewhere. ")
        
        if self.turn is Player.CROSS:
            self.cross |= bit
        else:
            self.nought |= bit

        self.turn = Player.NOUGHT if self.turn is Player.CROSS else Player.CROSS

    def is_win(self, bb: int) -> bool:
        # go through each pattern in the winning patterns for the given bitboard and return true if there is a win
        return any((bb & pattern) == pattern for pattern in WINNING_PATTERNS)

    def is_draw(self) -> bool:
        # if every cell is filled and neither cross or noughts have a win
        return self.occupied == 0b111111111 and not (self.is_win(self.cross) or self.is_win(self.nought))

    def state_key(self) -> int:
        # unique 18-bit int, for Q-table dict key
        return self.cross | (self.nought << 9)

    def to_grid(self) -> list[Player]:
        for i in range((SIZE * SIZE)):
            bit = 1 << i
            if self.cross & bit:
                self.grid[i] = Player.CROSS
            elif self.nought & bit:
                self.grid[i] = Player.NOUGHT
        return self.grid
    
    def generate_states(self):
        visited = set()
        queue = deque([(0, 0, SYMBOLS[Player.CROSS])])

        while len(queue) > 0:
            X_mask, O_mask, turn = queue.pop()
            state = (X_mask, O_mask)

            if state in visited:
                continue
            visited.add(state)

            is_full = (X_mask | O_mask) == FULL_BOARD
            if self.is_win(X_mask) or self.is_win(O_mask) or is_full:
                continue

            empty_mask = FULL_BOARD & ~(X_mask | O_mask) # 111111111 & ~(111110100) = 111111111 & 000001011 = 000001011 
            for bit in bits_of(empty_mask):
                if turn == SYMBOLS[Player.CROSS]:
                    queue.appendleft((X_mask | bit, O_mask, SYMBOLS[Player.NOUGHT])) 
                else:
                    queue.appendleft((X_mask, O_mask | bit, SYMBOLS[Player.CROSS]))

        return visited
    
    def render(self, cross: int, nought: int) -> str:
        s = ""
        for i in range(SIZE ** 2):
            if cross & (1 << i):
                s += SYMBOLS[Player.CROSS]
            elif nought & (1 << i):
                s += SYMBOLS[Player.NOUGHT]
            else:
                s  += "-"
            if i % SIZE < (SIZE - 1):
                s  += "|"
            elif i < ((SIZE ** 2) - 1):
                s  += "\n-----\n"
        return s

    def run(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Select a position on the board to place piece (1-9)")
        print(self.render(0, 0))

        while True:
            player = self.players[self.turn]
            pos = player.get_move(self)
            try:
                self.place_piece(pos)
            except ValueError as e:
                print(f"Invalid move: {e}")
                continue

            print(self.render(self.cross, self.nought))

            if self.is_win(self.cross):
                print("Cross won! Congrats.")
                break
            elif self.is_win(self.nought):
                print("Nought won! Yay.")
                break
            elif self.is_draw():
                print("Draw. Must've had optimal gameplay. Nerds...")
                break

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

if __name__ == "__main__":
    hp = HumanPlayer(); rp = RandomPlayer()
    env = Environment(hp, rp)
    env.run()



    # possible_states = env.generate_states()
    
    # print(len(possible_states))

    # for x in possible_states:
    #     env.cross, env.nought = x
        
    #     if ((env.cross | env.nought) == FULL_BOARD):
    #         print(env)
    #         print()
    #     elif env.is_win(env.cross) or env.is_win(env.nought):
            
    #         print(env)
    #         print()
    
    