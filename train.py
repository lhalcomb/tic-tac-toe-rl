from engine import Environment
from utils import Player 
from agents.agents import PolicyPlayer, RandomPlayer
from agents.valueiteration import ValueIteration

if __name__ == "__main__":

    def simulate_game(policy, agent: Player) -> str:
            opponent = Player.NOUGHT if agent is Player.CROSS else Player.CROSS
            players = {
                agent: PolicyPlayer(policy, agent),
                opponent: RandomPlayer(),
            }
            env = Environment(players[Player.CROSS], players[Player.NOUGHT])

            while True:
                player = env.players[env.turn]
                pos = player.get_move(env)
                env.place_piece(pos)

                if env.is_win(env.cross):
                    return "win" if agent is Player.CROSS else "loss"
                elif env.is_win(env.nought):
                    return "win" if agent is Player.NOUGHT else "loss"
                elif env.is_draw():
                    return "draw"


    def run_simulation(policy, agent: Player, n_games=100):
        results = {"win": 0, "loss": 0, "draw": 0}
        for _ in range(n_games):
            outcome = simulate_game(policy, agent)
            results[outcome] += 1
        print(results)
        assert results["loss"] == 0, f"Optimal policy should never lose, but lost {results['loss']} times"

    VI = ValueIteration()
    VI.value_iteration()
    run_simulation(VI.policy, agent=Player.CROSS, n_games=100)
        