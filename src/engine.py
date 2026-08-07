from utils.utility import Player, SIZE, WINNING_PATTERNS, FULL_BOARD, SYMBOLS, bits_of
from collections import deque 

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

if __name__ == "__main__":
    # Human VS Random
    from src.agents.players import HumanPlayer, RandomPlayer
    hp = HumanPlayer(); rp = RandomPlayer()
    env = Environment(hp, rp)
    env.run()

    



    
    
    