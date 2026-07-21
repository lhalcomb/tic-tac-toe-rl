# tic-tac-toe-rl

Applying reinforcement learning theory to the game of Tic-Tac-Toe.

The board is represented as a pair of 9-bit bitboards (one per player), with
game rules, state generation, and the play loop handled by an `Environment`
class. Players — human or agent — are pluggable, so any combination of
human-vs-human, human-vs-agent, or agent-vs-agent play is possible.

## Agents

- **Value & Policy Iteration** — classical dynamic-programming solutions
  over the full tic-tac-toe state space (~5,478 reachable states), used as
  a baseline for optimal play.
- **Q-Learning** — model-free tabular learning of state-action values
  through self-play.
- **MCTS** — Monte Carlo Tree Search, evaluating moves via simulated
  rollouts rather than a precomputed table.

Tic-Tac-Toe's small state space makes it a good testbed for comparing these
approaches before applying similar methods to larger games.


### Sources
- https://github.com/bsamseth/tic-tac-toe/blob/master/tictactoe.py
- Russell, S. J., and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th ed., Pearson, 2020.
- Sutton, Richard S., and Andrew G. Barto. *Reinforcement Learning: An Introduction*. 2nd ed., The MIT Press, 2018.
- https://huggingface.co/learn/deep-rl-course