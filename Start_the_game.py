from Player import Player
from HumanVSAI import HumanVSAI


def start_the_game():
    ai = Player("database_trained")
    HumanVSAI(ai).play()

