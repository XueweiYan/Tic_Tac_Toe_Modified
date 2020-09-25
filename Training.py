from IPython.display import clear_output


class Training:

    def __init__(self, player):
        self.player = player

    def train(self, num):
        self.reset_training()
        self.set_alpha(0.5)
        for _ in range(min(num, 10000)):
            if _ % 100 == 0:
                clear_output(wait=False)
                print('Training...')
            if _ % 10 == 0:
                print("Iteration:", _, "/", num)
            self.train_one_game()

        self.set_alpha(0.4)
        for _ in range(min(num, 10000), min(num, 100000)):
            if _ % 50 == 0:
                clear_output(wait=False)
                print("Training...")
            if _ % 5 == 0:
                print("Iteration:", _, "/", num)
            self.train_one_game()

        self.set_alpha(0.3)
        for _ in range(min(num, 100000), num):
            if _ % 10 == 0:
                clear_output(wait=False)
                print("Training...")
            print("Iteration:", _, "/", num)
            self.train_one_game()
        
        print("Finished!")
        self.finish_training()

    def train_one_game(self):
        ref_1 = self.player.start_new_game()
        ref_2 = self.player.second_move(ref_1)
        ref_3 = self.player.third_move(ref_2)
        ref_4 = self.player.fourth_move(ref_3)
        ref_5 = self.player.fifth_move(ref_4)
        if self.player.is_game_over(5, ref_5):
            return "Game Finished!"
        else:
            ref_6 = self.player.sixth_move(ref_5)

        symbol = ["X", "O"]
        flag = 0
        while not self.player.is_game_over(6, ref_6):
            ref_6 = self.player.further_move(ref_6, symbol[flag])
            flag = 1 - flag
        return "Game Finished!"

    def finish_training(self):
        self.player.set_epsilon(0)

    def reset_training(self):
        self.player.set_epsilon(0.5)

    def set_alpha(self, alpha):
        self.player.set_alpha(alpha)
