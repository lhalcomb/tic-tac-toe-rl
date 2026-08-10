### Utilities used in the tic tac toe logic ###
import json, os
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

def _encode_state(state: tuple) -> str: # json doesn't like tuples. 
    (X_mask, O_mask, turn) = state
    return f"{X_mask},{O_mask},{turn}"

def _decode_state(state: str) -> tuple:
    return tuple((int(x) if x.strip().isdigit() else x.strip() for x in state.split(",")))

############ Save/Load Policy ############

RV_SYMBOLS = {v: k for k, v in SYMBOLS.items()}

def save_policy(policy: dict, agent: Player, algo: str, gamma: float, eps: float, path: str):
    encoded_policy = {}
    
    for (state, action) in policy.items():
        encoded_state = _encode_state(state)
        encoded_policy[encoded_state] = action

    data = {
        "agent": SYMBOLS[agent],
        "mdp_algo": algo,
        "gamma": gamma,
        "eps": eps,
        "policy": encoded_policy,
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_policy(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)

    decoded_policy = {}
    for (key_str, action) in data["policy"].items():
        decoded_state = _decode_state(key_str)
        decoded_policy[decoded_state] = action

    agent = RV_SYMBOLS[data["agent"]]

    data["policy"] = decoded_policy
    data["agent"] = agent

    return data

def save_qtable(qtable: dict[tuple[int, int, str], dict], agent: Player, algo: str, gamma: float, eps: float, path: str):
    encoded_qtable = {}

    for state, action_values in qtable.items():
        encoded_state = _encode_state(state)
        encoded_qtable[encoded_state] = {str(action): value for action, value in action_values.items()}

    data = {
        "agent": SYMBOLS[agent],
        "mdp_algo": algo,
        "gamma": gamma,
        "eps": eps,
        "qtable": encoded_qtable,
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_qtable(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)

    decoded_qtable = {}
    for key_str, action_values in data["qtable"].items():
        decoded_state = _decode_state(key_str)
        decoded_qtable[decoded_state] = {int(action_str): value for action_str, value in action_values.items()}

    agent = RV_SYMBOLS[data["agent"]]

    data["qtable"] = decoded_qtable
    data["agent"] = agent

    return data

if __name__ == "__main__":
    for pattern in WINNING_PATTERNS:
        print(f"({pattern}, {pattern : b})", end=", ")

    print(RV_SYMBOLS)
    