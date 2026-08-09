import math

from src.agents.mdp import MDP, State, Player
from src.utils.utility import Player, FULL_BOARD, SYMBOLS, bits_of

class MiniMax(MDP): 
    def __init__(self, agent: Player):
        super().__init__(agent)

    def get_best_action(self, state: State):
        best_action = None
        best_value = -math.inf
        for action in self._get_actions(state):
            child_state = self.apply_action(state, action)
            value = self.minimax_alpha_beta(child_state, -math.inf, math.inf, False)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action

    def minimax_alpha_beta(self, state, alpha, beta, is_maximizing):
        if self.is_terminal(state):
            return self.evaluate(state, self.agent)
            
        if is_maximizing:
            max_evaluation = -float('inf')
            for action in self._get_actions(state):
                child_state = self.apply_action(state, action)
                evaluation = self.minimax_alpha_beta(child_state, alpha, beta, self.whose_turn(child_state) == self.agent)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  
            return max_evaluation
            
        else:
            min_evaluation = float('inf')
            for action in self._get_actions(state):
                child_state = self.apply_action(state, action)
                evaluation = self.minimax_alpha_beta(child_state, alpha, beta, self.whose_turn(child_state) == self.agent)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  

            return min_evaluation
        
    def evaluate(self, state, maximizing_player: Player) -> float:
        X_mask, O_mask, _ = state
        max_mask = X_mask if maximizing_player is Player.CROSS else O_mask
        min_mask = O_mask if maximizing_player is Player.CROSS else X_mask
        if self.is_win(max_mask):
            return 1.0
        elif self.is_win(min_mask):
            return -1.0
        else:
            return 0.0

    def apply_action(self, state: State, action: int):
        X_mask, O_mask, turn = state
        mover = self.whose_turn(state)
        X_after, O_after = (X_mask | action, O_mask) if mover is Player.CROSS else (X_mask, O_mask | action)
        next_turn = SYMBOLS[Player.NOUGHT] if mover is Player.CROSS else SYMBOLS[Player.CROSS]
        return (X_after, O_after, next_turn)

    def _get_actions(self, state: State):
        (X_mask, O_mask, _) = state
        if self.is_terminal(state):
            return []
        empty_mask = FULL_BOARD & ~(X_mask | O_mask)
        return list(bits_of(empty_mask))
