from src.agents.mdp import MDP, State
from src.utils.utility import Player, FULL_BOARD, bits_of

import random
from collections import defaultdict

class QLearning(MDP):
    def __init__(self, agent: Player, gamma: float, alpha: float, eps: float, num_of_episodes: int):
        super().__init__(agent, gamma)
        self.alpha = alpha
        self.eps = eps
        self.num_of_episodes = num_of_episodes
        self.Q_table = defaultdict(dict)  # Q_table[state][action] -> reward: float --> {state_0: {action_0: 0.0, action_1: 0.0, ...}, .... }

    def choose_action(self, state: State):
        if random.uniform(0, 1) < self.eps or state not in self.Q_table:
            # Exploration
            return random.choice(self._get_actions(state))
        else:
            # Exploitation
            #Choose the action with highest q_value from self.Q_table
            q_values = self.Q_table[state]
            best_action = max(q_values, key=q_values.get, default=None) #type: ignore
            if best_action is None:
                return random.choice(self._get_actions(state))
            return best_action

    def update_qtable(self, state, action, next_state, reward): # Q(s, a) <- Q(s, a) + alpha * (reward + gamma * max_a' Q(s', a') - Q(s, a))
        old_q = self.Q_table[state].get(action, 0.0)

        if self.is_terminal(next_state):
            target = reward   # no future value beyond a terminal state
        else:
            next_actions = self._get_actions(next_state)  # careful: whose turn is next_state?
            best_next_q = max(self.Q_table[next_state].get(a, 0.0) for a in next_actions)
            target = reward + self.gamma * best_next_q

        self.Q_table[state][action] = old_q + self.alpha * (target - old_q)

    def train(self):

        for _ in range(self.num_of_episodes):
            state = self.get_initial_state()
            while not self.is_terminal(state):
                action = self.choose_action(state)
                next_state_after_agent = self.apply_action(state, action)  # agent's move

                if self.is_terminal(next_state_after_agent):
                    reward = self.get_reward(state, action, next_state_after_agent)
                    self.update_qtable(state, action, next_state_after_agent, reward)
                    break

                opponent_actions = self._get_actions(next_state_after_agent)
                opponent_action = random.choice(opponent_actions)
                next_state = self.apply_action(next_state_after_agent, opponent_action)

                reward = self.get_reward(state, action, next_state)
                self.update_qtable(state, action, next_state, reward)
                state = next_state

            self.eps = max(self.eps * 0.995, 0.01)

    def update_qtable_self_play(self, state, action, next_state, reward):
        old_q_val = self.Q_table[state].get(action, 0.0)

        if self.is_terminal(next_state):
            target = reward
        else:
            next_actions = self._get_actions(next_state)
            best_next_q = max(self.Q_table[next_state].get(a, 0.0) for a in next_actions)
            target = reward - (self.gamma * best_next_q) # subtracting the reward from the update to force the agent to converge to best optimal value in self play

        self.Q_table[state][action] = old_q_val + self.alpha * (target - old_q_val)

    def train_self_play(self):
        for _ in range(self.num_of_episodes):
            state = self.get_initial_state()
            while not self.is_terminal(state):
                curr_turn = self.whose_turn(state)
                action = self.choose_action(state)
                next_state = self.apply_action(state, action)
                reward = self._reward_for_turn(curr_turn, next_state)
                self.update_qtable_self_play(state, action, next_state, reward)
                state = next_state

            self.eps = max(self.eps * 0.995, 0.01)

    ##### Private Helper Methods #####
    def _get_actions(self, state: State):
        (X_mask, O_mask, _) = state
        if self.is_terminal(state):
            return []
        empty_mask = FULL_BOARD & ~(X_mask | O_mask)
        return list(bits_of(empty_mask))

    def _reward_for_turn(self, turn: Player, next_state: State):
        if not self.is_terminal(next_state):
            return 0.0
        
        X_next, O_next, _ = next_state
        turn_mask = X_next if turn is Player.CROSS else O_next
        opp_mask = O_next if turn is Player.CROSS else X_next

        if self.is_win(turn_mask):
            return 1.0
        elif self.is_win(opp_mask):
            return -1.0
        else:
            return 0.0

if __name__ == "__main__":

    ql = QLearning(Player.CROSS, 0.95, 0.9, 0.8, 1000)
    print(ql.choose_action((34, 65, 'X')))
