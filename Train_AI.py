from Player import Player
from Training import Training


def train_ai():
    num_train = int(input("How many iterations for training?"))
    ai = Player("database_initial")
    training = Training(ai)

    training.train(num_train)
    ai.save_dfs("database_trained")