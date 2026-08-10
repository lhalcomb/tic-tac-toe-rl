from src.utils.utility import Player, SYMBOLS, save_policy, save_qtable
from src.agents.players import RandomPlayer, PolicyPlayer, QLearningPlayer
from src.agents.valueiteration import ValueIteration
from src.agents.policyiteration import PolicyIteration
from src.agents.q_learning import QLearning
from .evaluate import PolicyEvaluator


class Trainer:
    def __init__(self, agent: Player, mdp_algo: str):
        self.agent = agent
        self.mdp_algo = mdp_algo
        self.policy = None

        self.QTable: dict[tuple[int, int, str], dict] | None = None

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
        elif self.mdp_algo == "QLearning":
            QL = QLearning(self.agent, 0.99, 0.2, 1.0, 40000)
            QL.train_self_play()
            self.QTable = QL.Q_table
            gamma, eps = QL.gamma, QL.eps
        else:
            raise ValueError(f"Unknown mdp_algo: {self.mdp_algo!r}")

        if save and self.mdp_algo != "QLearning":
            path = f"policies/{self.mdp_algo.lower()}_{SYMBOLS[self.agent]}.json"
            save_policy(self.policy, self.agent, self.mdp_algo, gamma, eps, path)  #type: ignore

        elif save and self.mdp_algo == "QLearning":
            path = f"policies/{self.mdp_algo.lower()}_{SYMBOLS[self.agent]}.json"
            save_qtable(self.QTable, self.agent, self.mdp_algo, gamma, eps, path) #type: ignore

        return self.QTable if self.mdp_algo == "QLearning" else self.policy
if __name__ == "__main__":

    #Test VI
    # trainVI = Trainer(Player.NOUGHT, "ValueIteration")
    # VIpolicy = trainVI.train()
    # policyPlayerVI = PolicyPlayer(VIpolicy, trainVI.agent); rand = RandomPlayer() #type: ignore
    # evaluator = PolicyEvaluator(policyPlayerVI, rand, trainVI.agent)
    # results = evaluator.run_simulation()
    # print(results)
    #assert results["loss"] == 0, f"Optimal policy should never lose, but lost {results['loss']} times"

    #Test PI
    # trainPI = Trainer(Player.CROSS, "PolicyIteration")
    # PIpolicy = trainPI.train(True)
    # policyPlayerPI = PolicyPlayer(PIpolicy, trainPI.agent); rand = RandomPlayer() #type: ignore
    # evaluator = PolicyEvaluator(policyPlayerPI, rand, trainPI.agent)
    # results = evaluator.run_simulation()
    # print(results)
    #assert results["loss"] == 0, f"Optimal policy should never lose, but lost {results['loss']} times"

    #Train Q-Learning
    trainQL = Trainer(Player.NOUGHT, "QLearning")
    QLtable = trainQL.train(True)
    print(len(trainQL.QTable), "states in table") #type: ignore
    QLearningPlayer_ = QLearningPlayer(trainQL.QTable, trainQL.agent); rand = RandomPlayer() #type: ignore
    evaluator = PolicyEvaluator(QLearningPlayer_, rand, trainQL.agent)
    results = evaluator.run_simulation(100)
    print(results)