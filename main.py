import argparse
from src.agents.players import *
from src.engine import Environment
from src.utils.utility import load_policy

def load_policy_player(path: str) -> PolicyPlayer:
    data = load_policy(path)
    return PolicyPlayer(data["policy"], data["agent"])

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

    vp_x = "/Users/laydenhalcomb/TicTacToe/tic-tac-toe-rl/policies/valueiteration_X.json"
    vp_o = "/Users/laydenhalcomb/TicTacToe/tic-tac-toe-rl/policies/valueiteration_O.json"
    pp_x = "/Users/laydenhalcomb/TicTacToe/tic-tac-toe-rl/policies/policyiteration_X.json"
    pp_o = "/Users/laydenhalcomb/TicTacToe/tic-tac-toe-rl/policies/policyiteration_O.json"

    agent_choices = {"Human": HumanPlayer(), "ValueIteration_X": load_policy_player(vp_x), "ValueIteration_O": load_policy_player(vp_o) , 
                     "PolicyIteration_X": load_policy_player(pp_x), "PolicyIteration_O": load_policy_player(pp_o), 
                     "MiniMax_X": MiniMaxPlayer(Player.CROSS), "MiniMax_O": MiniMaxPlayer(Player.NOUGHT)} #, "Q-Learning"

    print(f"Aglorithm Choices {list(agent_choices)} ")
    print("From the list above, choose your player.")

    player_x = input("Which algorithm is the cross: ")
    player_o = input("Which algorithm is the nought: ")

    player_x = agent_choices[player_x]
    player_o = agent_choices[player_o]

    env = Environment(player_x, player_o)
    env.run()


