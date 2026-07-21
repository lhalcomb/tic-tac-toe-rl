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
