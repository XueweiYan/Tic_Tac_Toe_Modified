class GamePlay:

    def __init__(self, player):
        self.player = player

    def play(self):
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

