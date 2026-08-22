from src.utils.utility import Player, WINNING_PATTERNS, FULL_BOARD, SYMBOLS, bits_of,hamWeight
from collections import deque

### Type Alias' ###
type State = tuple[int, int, str]

class MDP:
    def __init__(self, agent: Player = Player.CROSS, gamma: float = 0.95):
        self.agent = agent
        self.opponent = Player.NOUGHT if agent is Player.CROSS else Player.CROSS
        self.gamma = gamma
        self._states = set()
        self._terminal = set()

    def get_states(self): # S
        queue = deque([(0, 0, SYMBOLS[Player.CROSS])])

        while len(queue) > 0:
            X_mask, O_mask, turn = queue.pop()
            state = (X_mask, O_mask, turn)

            if state in self._states:
                continue
            self._states.add(state)

            is_full = (X_mask | O_mask) == FULL_BOARD
            if self.is_win(X_mask) or self.is_win(O_mask) or is_full:
                continue

            empty_mask = FULL_BOARD & ~(X_mask | O_mask) # 111111111 & ~(111110100) = 111111111 & 000001011 = 000001011 
            for bit in bits_of(empty_mask):
                if turn == SYMBOLS[Player.CROSS]:
                    queue.appendleft((X_mask | bit, O_mask, SYMBOLS[Player.NOUGHT])) 
                else:
                    queue.appendleft((X_mask, O_mask | bit, SYMBOLS[Player.CROSS]))

    def get_initial_state(self): # s_0
        return (0, 0, SYMBOLS[self.agent])  # empty board, X to move

    def is_terminal(self, state: State) -> bool:
        X_mask, O_mask, _ = state
        return self.is_win(X_mask) or self.is_win(O_mask) or (X_mask | O_mask) == FULL_BOARD

    def is_win(self, bb: int) -> bool:
        return any((bb & pattern) == pattern for pattern in WINNING_PATTERNS)

    def whose_turn(self, state: State) -> Player:
        X_mask, O_mask, _ = state
        return Player.CROSS if hamWeight(X_mask) == hamWeight(O_mask) else Player.NOUGHT #x_count = bin(X_mask).count("1") o_count = bin(O_mask).count("1")

    def get_actions(self, state: State): # A(s)
       (X_mask, O_mask, turn) = state
       if self.is_terminal(state):
           return []
       if turn != SYMBOLS[self.agent]: #we dont care about the other guys actions
           return []
       empty_mask = FULL_BOARD & ~(X_mask | O_mask)
       return list(bits_of(empty_mask)) # return the actions that can be taken from the state given as bits

    def get_transitions(self, state: State, action: int) -> list[tuple[State, float]]: #P
        X_mask, O_mask, _ = state
        # apply the action based on the agent that was set (X or O) 
        X_after, O_after = (X_mask | action, O_mask) if self.agent is Player.CROSS else (X_mask, O_mask | action)

        # if the agent's move ended the game, return the last state it placed along with the opponent's turn
        is_full = (X_after | O_after) == FULL_BOARD
        if self.is_win(X_after) or self.is_win(O_after) or is_full:
            return [((X_after, O_after, SYMBOLS[self.opponent]), 1.0)]
        
        # turn empty cells (actions) into 1 bits and get the respective action probability at that state using 1/their hamming weight (1bit count) (every action is equally likely at every state)
        empty_mask = FULL_BOARD & ~(X_after | O_after)
        prob = 1 / hamWeight(empty_mask)

        # opponent's turn: iterate through every action the opponent could choose
        next_states = []
        for action in bits_of(empty_mask): 
            X_next, O_next = (X_after | action, O_after) if self.opponent is Player.CROSS else (X_after, O_after | action) # get the next action from the opponent
            next_states.append(((X_next, O_next, SYMBOLS[self.agent]), prob)) #append it to next states with the respective probability of choosing that action
        return next_states

    def get_reward(self, state: State, action: int, next_state: State) -> float: #R
        """
        Reward from self.agent's perspective. Only really nonzero
        when next_state is terminal:
          agent wins  -> +1
          opponent wins -> -1
          draw          ->  0
        Everything else (non-terminal next_state) -> 0.
        """
        if not self.is_terminal(next_state):
            return 0.0

        X_next, O_next, _ = next_state
        agent_mask = X_next if self.agent is Player.CROSS else O_next
        opp_mask = O_next if self.agent is Player.CROSS else X_next

        if self.is_win(agent_mask):
            return 1.0
        elif self.is_win(opp_mask):
            return -1.0
        else:
            return 0.0  # draw

    def get_discount_factor(self) -> float: #gamma
        return self.gamma

    # public helper
    def apply_action(self, state: State, action: int):
        X_mask, O_mask, turn = state
        mover = self.whose_turn(state)
        X_after, O_after = (X_mask | action, O_mask) if mover is Player.CROSS else (X_mask, O_mask | action)
        next_turn = SYMBOLS[Player.NOUGHT] if mover is Player.CROSS else SYMBOLS[Player.CROSS]
        return (X_after, O_after, next_turn)
    

if __name__ == "__main__":
    import random
    
    mdp = MDP()
    mdp.get_states()
    print(len(mdp._states))
    # for i in mdp._states:
    #     print(i)
    print(random.choice(list(mdp._states)[4]))
    print(mdp.get_actions(random.choice(list(mdp._states))))
    # print(list(mdp._states))
    print(f"{34:b}, {65:b}")
    transitions = []
    for action in mdp.get_actions((34, 65, 'X')):
        transitions.append(mdp.get_transitions((34, 65, 'X'), action))
    print(len(transitions))
    print(len(transitions[1]))
    next_state = mdp.get_transitions((34, 65, 'X'), mdp.get_actions((34, 65, 'X'))[1])
    print(mdp.get_reward((34, 65, 'X'),mdp.get_actions((34, 65, 'X'))[1], next_state[0][0]))
    
