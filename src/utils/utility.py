### Utilities used in the tic tac toe logic ###
import json
import os
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

def _encode_state(state: tuple) -> list: # json doesn't like tuples. 
    (X_mask, O_mask, turn) = state
    return [list(state), f"{X_mask},{O_mask},{turn}"]

def _decode_state(state: list) -> tuple:
    return tuple(state[0])

############ Save/Load Policy ############

RV_SYMBOLS = {v: k for k, v in SYMBOLS.items()}

def save_policy(policy: dict, agent: Player, algo: str, gamma: float, eps: float, path: str):
    """
    eg. use in Trainer(...) - save_policy(self.policy, self.agent, self.mdp_algo, VI.gamma, VI.eps,
            path=f"policies/{self.mdp_algo.lower()}_{SYMBOLS[self.agent]}.json")

    Wrap policy + metadata into one JSON-serializable dict and write it.
    - encode every key in `policy` via _encode_state
    - build the wrapper: {"agent": ..., "mdp_algo": ..., "gamma": ...,
      "eps": ..., "policy": {...}}
    - os.makedirs(os.path.dirname(path), exist_ok=True) so policies/
      doesn't need to exist beforehand
    - json.dump(..., f) — consider indent=2 for readability since you
      wanted this human-inspectable
    """
    pass

def load_policy(path: str) -> dict:
    """
    Read the JSON file back, decode every key in the "policy" sub-dict
    via _decode_state, and return the FULL wrapper dict (not just the
    policy) — main.py will want agent/mdp_algo/gamma/eps too, not just
    the raw policy mapping. Caller does result["policy"] if they just
    want the moves.
    """
    return {}


if __name__ == "__main__":
    # for pattern in WINNING_PATTERNS:
    #     print(f"({pattern}, {pattern : b})", end=", ")

    # print(RV_SYMBOLS)
    pass