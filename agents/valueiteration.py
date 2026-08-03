from mdp import MDP, State, SYMBOLS, Player, WINNING_PATTERNS, hamWeight

class ValueIteration(MDP):
    def __init__(self, eps: float = 10e-6):
        super().__init__()
        self.get_states()
        self.eps = eps
        self.V: dict[State, float]  = {state: 0 for state in self._states} # initialize every value at every state to 0
        self.policy = {state: self.get_actions(state)[0] for state in self._states if self.get_actions(state)} #initialize the policy dict to a random action before updating for max action at a state
    
    def q_value(self, state, action, V):
        return sum(
            prob * (self.get_reward(state, action, ns) + self.get_discount_factor() * V[ns])
            for ns, prob in self.get_transitions(state, action)
        )
    
    def extract_policy(self, V: dict[State, float]) -> dict:
        policy = {}
        for state in self._states:
            actions = self.get_actions(state)
            if not actions:
                continue
            policy[state] = max(actions, key=lambda a: self.q_value(state, a, V)) 
        return policy

    def bellman_update(self, state: State, V: dict[State, float]) -> float:
        actions = self.get_actions(state)
        if not actions:
            return 0.0
        return max(self.q_value(state, action, V) for action in actions)

    def value_iteration(self, max_iterations = 100):
        for _ in range(max_iterations): 
            new_values = {}
            for state in self._states:
                new_values[state] = self.bellman_update(state, self.V)
            if max(abs(new_values[s] - self.V[s]) for s in self._states) < self.eps:
                self.V = new_values
                break
            self.V = new_values
        self.policy = self.extract_policy(self.V)
        
if __name__ == "__main__":

    VI = ValueIteration()
    policy_dict = VI.policy
    print(policy_dict)
    print(len(policy_dict))
    for state in policy_dict:
        print(VI.get_actions(state))
    
    value_dict = VI.V
    print(len(value_dict))
    for state in value_dict:
        print(VI.get_actions(state))

    print(len(VI._states))
    sample = next(iter(VI._states))
    print(sample)
    print(VI.get_actions(sample))

    VI.value_iteration()

    for state in VI._states:
        X_mask, O_mask, turn = state
        if turn != SYMBOLS[Player.CROSS]:
            continue
        for pattern in WINNING_PATTERNS:
            missing = pattern & ~X_mask
            if hamWeight(pattern & X_mask) == 2 and hamWeight(missing) == 1 and not (missing & O_mask):
                print(state)
                print("V:", VI.V[state])
                print("policy action:", VI.policy.get(state))
                break
        else:
            continue
        break

    