
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

# I like to print all of my constants at the top. B/c once upon a time I learned C.
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
    def __init__(self): 

        self.cross: int = 0   # bitmask of X positions
        self.nought: int = 0  # bitmask of O positions

        self.bitboards = [self.cross, self.nought]
        self.turn = Player.CROSS

        self.grid = [Player.EMPTY] * (SIZE * SIZE)
    
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
    
class Agent: 
    def __init__(self):
        pass

if __name__ == "__main__":
    env = Environment()
    
    possible_states = env.generate_states()
    
    print(len(possible_states))

    for x in possible_states:
        env.cross, env.nought = x
        
        if ((env.cross | env.nought) == FULL_BOARD):
            print(env)
            print()
        elif env.is_win(env.cross) or env.is_win(env.nought):
            
            print(env)
            print()
    