from src.engine import Environment
from utils.utility import Player

class PolicyEvaluator:
    def __init__(self, agent_player, opponent_player, agent_symbol: Player):
        self.agent_symbol = agent_symbol
        self.players = {
            agent_symbol: agent_player,
            (Player.NOUGHT if agent_symbol is Player.CROSS else Player.CROSS): opponent_player,
        }

    def simulate_game(self) -> str:
        env = Environment(self.players[Player.CROSS], self.players[Player.NOUGHT])
        while True:
            player = env.players[env.turn]
            pos = player.get_move(env)
            env.place_piece(pos)
            if env.is_win(env.cross):
                return "win" if self.agent_symbol is Player.CROSS else "loss"
            elif env.is_win(env.nought):
                return "win" if self.agent_symbol is Player.NOUGHT else "loss"
            elif env.is_draw():
                return "draw"

    def run_simulation(self, n_games=100):
        results = {"win": 0, "loss": 0, "draw": 0}
        for _ in range(n_games):
            results[self.simulate_game()] += 1
        return results
        