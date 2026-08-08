from src.agents.mdp import MDP, State, Player

class PolicyIteration(MDP):
    def __init__(self, agent: Player = Player.CROSS, eps: float = 10e-6, max_iterations=100):
        super().__init__(agent)
        self.get_states()
        self.max_iterations = max_iterations
        self.eps = eps
        self.V: dict[State, float]  = {state: 0 for state in self._states} # initialize every value at every state to 0
        self.policy = {state: self.get_actions(state)[0] for state in self._states if self.get_actions(state)} #initialize the policy dict to a random action before updating for max action at a state
    
    def q_value(self, state, action, V):
        return sum(
            prob * (self.get_reward(state, action, ns) + self.get_discount_factor() * V[ns])
            for ns, prob in self.get_transitions(state, action)
        )
    
    def policy_evaluation(self):
        for _ in range(self.max_iterations):
            new_values = {}
            for state in self._states:
                if state not in self.policy:
                    new_values[state] = 0.0
                else:
                    action = self.policy[state]
                    new_values[state] = self.q_value(state, action, self.V)
            delta = max(abs(new_values[s] - self.V[s]) for s in self._states)
            self.V = new_values
            if delta < self.eps:
                break

    def policy_improvement(self):
        policy_stable = True
        for state in self._states:
            actions = self.get_actions(state)
            if not actions:
                continue
            old_action = self.policy.get(state)
            best_action = max(actions, key=lambda a: self.q_value(state, a, self.V))
            self.policy[state] = best_action
            if best_action != old_action:
                policy_stable = False
        return policy_stable
    
    def policy_iteration(self):
        for _ in range(self.max_iterations):
            self.policy_evaluation()
            stable = self.policy_improvement()
            if stable:
                break
        