from src.agents.players import *
from src.engine import Environment

from pathlib import Path
from src.utils.utility import load_policy, load_qtable

def load_policy_player(path: Path) -> PolicyPlayer:
    data = load_policy(path)
    return PolicyPlayer(data["policy"], data["agent"])

def load_qtable_player(path: Path) -> QLearningPlayer:
    data = load_qtable(path)
    return QLearningPlayer(data["qtable"], data["agent"])

if __name__ == "__main__":
    # _ = None
    # env = Environment(_, _)
    # possible_states = env.generate_states()
    
    # print(len(possible_states))
    # wins = 0; ties = 0; losses = 0

    # for x in possible_states:
    #     env.cross, env.nought = x
        
    #     if (env.is_draw()):
    #         ties += 1
    #         print(env)
    #         print()
    #     elif env.is_win(env.cross) or env.is_win(env.nought):
    #         wins += 1
    #         print(env)
    #         print()
    #     else: 
    #         losses += 1

    # print(f"Wins: {wins}")
    # print(f"Draws: {ties}")
    # print(f"Losses: {losses}")
    PROJECT_ROOT = Path(__file__).resolve().parent

    vp_x = PROJECT_ROOT / "policies" / "valueiteration_X.json"
    vp_o = PROJECT_ROOT / "policies" / "valueiteration_O.json"
    pp_x = PROJECT_ROOT / "policies" / "policyiteration_X.json"
    pp_o = PROJECT_ROOT / "policies" / "policyiteration_O.json"
    ql_x = PROJECT_ROOT / "policies" / "qlearning_X.json"
    ql_o = PROJECT_ROOT / "policies" / "qlearning_O.json"

    agent_factories = {
    "Human": lambda _: HumanPlayer(),
    "ValueIteration": lambda agent: load_policy_player(vp_x if agent is Player.CROSS else vp_o),
    "PolicyIteration": lambda agent: load_policy_player(pp_x if agent is Player.CROSS else pp_o),
    "MiniMax": lambda agent: MiniMaxPlayer(agent),
    "QLearning": lambda agent: load_qtable_player(ql_x if agent is Player.CROSS else ql_o),
    "MCTS": lambda agent: MCTSPlayer(agent)
    }

    print(f"Algorithm choices: {list(agent_factories)}")
    choice_x = input("Which algorithm is the cross: ")
    choice_o = input("Which algorithm is the nought: ")

    player_x = agent_factories[choice_x](Player.CROSS)
    player_o = agent_factories[choice_o](Player.NOUGHT)

    env = Environment(player_x, player_o)
    env.run()


