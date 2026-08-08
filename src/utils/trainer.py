from src.utils.utility import Player, SYMBOLS, save_policy
from src.agents.players import RandomPlayer, PolicyPlayer
from src.agents.valueiteration import ValueIteration
from src.agents.policyiteration import PolicyIteration
from .evaluate import PolicyEvaluator


class Trainer:
    def __init__(self, agent: Player, mdp_algo: str):
        self.agent = agent
        self.mdp_algo = mdp_algo
        self.policy = None

    def train(self, save=True):
        if self.mdp_algo == "ValueIteration":
            VI = ValueIteration(agent=self.agent)
            VI.value_iteration()
            self.policy = VI.policy
            gamma, eps = VI.gamma, VI.eps
        elif self.mdp_algo == "PolicyIteration":
            PI = PolicyIteration(agent=self.agent)
            PI.policy_iteration()
            self.policy = PI.policy
            gamma, eps = PI.gamma, PI.eps
        else:
            raise ValueError(f"Unknown mdp_algo: {self.mdp_algo!r}")

        if save:
            path = f"policies/{self.mdp_algo.lower()}_{SYMBOLS[self.agent]}.json"
            save_policy(self.policy, self.agent, self.mdp_algo, gamma, eps, path)

        return self.policy
if __name__ == "__main__":

    #Test VI
    trainVI = Trainer(Player.CROSS, "ValueIteration")
    VIpolicy = trainVI.train()
    policyPlayerVI = PolicyPlayer(VIpolicy, trainVI.agent); rand = RandomPlayer()
    evaluator = PolicyEvaluator(policyPlayerVI, rand, trainVI.agent)
    results = evaluator.run_simulation()
    print(results)
    assert results["loss"] == 0, f"Optimal policy should never lose, but lost {results['loss']} times"

    #Test PI
    trainPI = Trainer(Player.NOUGHT, "PolicyIteration")
    PIpolicy = trainPI.train(True)
    policyPlayerPI = PolicyPlayer(PIpolicy, trainPI.agent); rand = RandomPlayer()
    evaluator = PolicyEvaluator(policyPlayerPI, rand, trainPI.agent)
    results = evaluator.run_simulation()
    print(results)
    assert results["loss"] == 0, f"Optimal policy should never lose, but lost {results['loss']} times"