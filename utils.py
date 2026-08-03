### Utilities used in the tic tac toe logic ###

from enum import Enum

########## ENUMS/STRUCTS ##########
class Player(Enum):
    EMPTY = 0
    CROSS = 1
    NOUGHT = 2

############ CONSTANTS ############
SIZE = 3
# Winning patterns encoded in bit patterns.
# E.g. three in a row in the top row is
#   448 = 0b111000000
# (448,  111000000), (56,  111000), (7,  111), (292,  100100100), (146,  10010010), (73,  1001001), (273,  100010001), (84,  1010100)
WINNING_PATTERNS = [
        0b111000000, 0b111000, 0b111,   # Rows
        0b100100100, 0b10010010, 0b1001001, # Columns
        0b100010001, 0b1010100       # Diagonals
]
FULL_BOARD = 0b111111111

SYMBOLS = {Player.EMPTY: ".", Player.CROSS: "X", Player.NOUGHT: "O"}

############ Helper Functions ############
def bits_of(mask: int):
    while mask:
        low = mask & -mask
        yield low     # pause here, hand back `low`, remember where we are
        mask = mask ^ low   # resumes here on the *next* call

def to_relative(X_mask: int, O_mask: int, turn: Player) -> tuple[int, int]:
    return (X_mask, O_mask) if turn is Player.CROSS else (O_mask, X_mask)

def hamWeight(bitboard: int) -> int:
    n = bitboard
    count = 0
    while n:
        n = n & (n - 1)
        count += 1
    return count

if __name__ == "__main__":
    for pattern in WINNING_PATTERNS:
        print(f"({pattern}, {pattern : b})", end=", ")