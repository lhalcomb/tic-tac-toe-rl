from tictactoerl import Environment, AgentPlayer, RandomPlayer, HumanPlayer


if __name__ == "__main__":
    _ = None
    env = Environment(_, _)
    possible_states = env.generate_states()
    
    print(len(possible_states))
    wins = 0; ties = 0; losses = 0

    for x in possible_states:
        env.cross, env.nought = x
        
        if (env.is_draw()):
            ties += 1
            print(env)
            print()
        elif env.is_win(env.cross) or env.is_win(env.nought):
            wins += 1
            print(env)
            print()
        else: 
            losses += 1

    print(f"Wins: {wins}")
    print(f"Draws: {ties}")
    print(f"Losses: {losses}")