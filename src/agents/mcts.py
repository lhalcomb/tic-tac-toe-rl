from __future__ import annotations

import math, random

from src.agents.mdp import MDP, State, Player
from src.utils.utility import Player, FULL_BOARD, SYMBOLS, bits_of

class MCTSNode(MDP):
    def __init__(self, state: State, parent: MCTSNode | None, action: int, player: Player):
        self.state = state
        self.parent = parent
        self.action = action
        self.player = player
        self.children: list[MCTSNode] = []
        self.visits: int = 0 # number of times a node was visited
        self.wins: float = 0.0  #total reward from simulation
        
        self.untried_actions: list[int] = self._get_actions(self.state)
    
    def _terminal_state(self, state: State) -> bool:
        return self.is_terminal(state)
    
    def _is_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0
    
    def ucb(self, child: MCTSNode, c: float) -> float:
        return (child.wins / child.visits) + (c * math.sqrt(math.log(self.visits) / child.visits ) )
    
    def _best_child(self, c: float = math.sqrt(2)):
        for child in self.children: #if you havent visisted the node yet, select it
            if child.visits == 0: 
                return child
        return max(self.children, key = lambda child: self.ucb(child, c))

    ##### Helper Methods #####

    def _get_actions(self, state: State):
        (X_mask, O_mask, _) = state
        if self.is_terminal(state):
            return []
        empty_mask = FULL_BOARD & ~(X_mask | O_mask)
        return list(bits_of(empty_mask))

class MCTS(MDP):
    def __init__(self, agent: Player, time: int = 500):
        super().__init__(agent)
        self.time = time
        self.root: MCTSNode | None = None

    def search(self, state: State) -> int: #the mcts search
        self.root = MCTSNode(
            state=state,
            parent=None,
            action=0, # root has no incoming action
            player= self.agent
        )

        for _ in range(self.time):
            node = self._select(self.root)
            node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)

        if not self.root.children:
            return 0  # no legal moves, pass the turn
        
        # pick the child of root with the most visits
        best = max(self.root.children, key=lambda n: n.visits) 
        return best.action

    def _select(self, node: MCTSNode) -> MCTSNode:

        while not node._terminal_state(node.state) and node._is_fully_expanded():
            if not node.children:  # fully expanded but no children = terminal
                return node
            node = node._best_child()
        
        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        if not node.untried_actions:
            return node
        
        action = node.untried_actions.pop()
        new_state = self.apply_action(node.state, action)
        next_player = self.whose_turn(new_state)
        # current_player = node.state

        child = MCTSNode(new_state, node, action, next_player)
        node.children.append(child)

        return child

    def _simulate(self, node: MCTSNode) -> float:
        curr_state = node.state

        while not self.is_terminal(curr_state): 
            actions = node._get_actions(curr_state)
            if not actions:
                break

            action = random.choice(actions)
            curr_state = self.apply_action(curr_state, action)

        return self._evaluate_terminal_state(curr_state)
    
    def _backpropagate(self, node: MCTSNode| None, result: float) -> None:
        if node is not None and node.player == self.agent:
            result = -result

        while node is not None:
            node.visits += 1
            node.wins += result #accumulate the result (reward)
            result = -result
            node = node.parent 
        
    def _evaluate_terminal_state(self, state: State) -> float:
        X_mask, O_mask, _ = state
        prop_mask = X_mask if self.agent is Player.CROSS else O_mask
        opp_mask = O_mask if self.agent is Player.CROSS else X_mask
        if self.is_win(prop_mask):
            return 1.0
        elif self.is_win(opp_mask):
            return -1.0
        else:
            return 0.0

if __name__ == "__main__":
    mcts = MCTS(Player.CROSS)
    best_action = mcts.search((34, 65, 'X'))
    print(best_action)