import time
from IPython.display import clear_output


class HumanVSAI:

    def __init__(self, ai_player):
        self.ai = ai_player

    def play(self):
        intro = input("Wanna read the rule of this game[y/n]?\n")
        while intro not in ["y", "n"]:
            intro = input("Invalid input...\nWanna read the rule of this game[y/n]?\n")
        if intro == "y":
            # Intro
            clear_output(wait=False)
            print("Tic-Tac-Toe Modified\n")
            time.sleep(2)
            print("The rule follows the classic Tic-Tac-Toe game, except that...")
            time.sleep(3)
            print("only three markers are available for each player...")
            time.sleep(4)
            print("The first three moves follow the basic rule of the classic Tic-Tac-Toe game,")
            time.sleep(4)
            print("but starting from the fourth move,")
            time.sleep(3)
            print("each player HAS TO relocate one of their markers on board to ANOTHER empty space.")
            time.sleep(5)
            print("Enjoy :)")
            time.sleep(8)

        restart = True
        while restart:
            clear_output(wait=False)
            print("The game starts!\n")
            time.sleep(0.1)
            first_hand = input("Do you want to be the starting player[y/n]?\n")
            while first_hand not in ["y", "n"]:
                first_hand = input("Invalid input...\nDo you want to be the starting player[y/n]?\n")
            if first_hand == "y":
                self.play_as_first_hand()
            else:
                self.play_as_second_hand()
            time.sleep(0.1)
            again = input("Another game [y/n]?\n")
            while again not in ["y", "n"]:
                again = input("Invalid input...\nDo you want another game [y/n]?\n")
            restart = again == "y"
        clear_output(wait=False)
        print("GG, see you next time!")

    def play_as_first_hand(self):
        clear_output(wait=False)
        time.sleep(1)

        # New board
        row = 0
        current_state = self.ai.df_0.loc[row, range(9)]
        self.ai.display_board(0, row)
        time.sleep(1)

        # Ask First move
        first_move = int(input("Your first move(1~9)?\n")) - 1
        while (first_move not in range(9)) or (current_state[first_move] != " "):
            first_move = int(input("Invalid input...\nYour first move(1~9)?\n")) - 1

        # Execute first move
        clear_output(wait=False)
        time.sleep(1)
        current_state[first_move] = "X"
        row = self.ai.df_1.index[(self.ai.df_1[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(1, row)

        # AI second move
        row = self.ai.second_move(row)
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_2.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(2, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(2, row)
        time.sleep(1)

        # Ask third move
        third_move = int(input("Your second move(1~9)?\n")) - 1
        while (third_move not in range(9)) or (current_state[third_move] != " "):
            third_move = int(input("Invalid input...\nYour second move(1~9)?\n")) - 1

        # Execute third move
        clear_output(wait=False)
        time.sleep(1)
        current_state[third_move] = "X"
        row = self.ai.df_3.index[(self.ai.df_3[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(3, row)

        # AI fourth move
        row = self.ai.fourth_move(row)
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_4.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(4, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(4, row)
        time.sleep(1)

        # Ask fifth move
        fifth_move = int(input("Your third move(1~9)?\n")) - 1
        while (fifth_move not in range(9)) or (current_state[fifth_move] != " "):
            fifth_move = int(input("Invalid input...\nYour third move(1~9)?\n")) - 1

        # Execute fifth move
        clear_output(wait=False)
        time.sleep(1)
        current_state[fifth_move] = "X"
        row = self.ai.df_5.index[(self.ai.df_5[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(5, row)
        if self.ai.is_game_over(5, row):  # test for winning
            print("You win!\n")
            return

        # AI sixth move
        row = self.ai.sixth_move(row)
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_6.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(6, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(6, row)
        if self.ai.is_game_over(6, row):
            print("You lose!\n")
            return
        time.sleep(1)

        # Now moving instead of adding
        while True:
            # Ask human move
            remove = int(input("Remove your marker from (1~9)?\n")) - 1
            while (remove not in range(9)) or (current_state[remove] != "X"):
                remove = int(input("Invalid input...\nRemove your marker from (1~9)?\n")) - 1
            locate = int(input("Relocate your marker into (1~9)?\n")) - 1
            while (locate not in range(9)) or (current_state[locate] != " "):
                locate = int(input("Invalid input...\nRelocate your marker into (1~9)?\n")) - 1

            # Execute human move
            clear_output(wait=False)
            time.sleep(1)
            current_state[remove] = " "
            current_state[locate] = "X"
            row = self.ai.df_6.index[(self.ai.df_6[range(9)] == current_state).all(axis=1)][0]
            self.ai.display_board(6, row)
            if self.ai.is_game_over(6, row):
                print("You win!\n")
                break

            # AI move
            row = self.ai.further_move(row, "O")
            time.sleep(1)  # Fak thinking
            current_state = self.ai.df_6.loc[row, range(9)]
            clear_output(wait=False)
            self.ai.display_board(6, row)
            time.sleep(0.1)  # Blink effect as notification
            clear_output(wait=False)
            self.ai.display_board(6, row)
            if self.ai.is_game_over(6, row):
                print("You lose!\n")
                return
            time.sleep(1)
        return

    def play_as_second_hand(self):
        clear_output(wait=False)
        time.sleep(1)

        # New board
        row = 0
        current_state = self.ai.df_0.loc[row, range(9)]
        self.ai.display_board(0, row)
        time.sleep(1)

        # AI first move
        row = self.ai.start_new_game()
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_1.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(1, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(1, row)
        time.sleep(1)

        # Ask Second move
        second_move = int(input("Your first move(1~9)?\n")) - 1
        while (second_move not in range(9)) or (current_state[second_move] != " "):
            second_move = int(input("Invalid input...\nYour first move(1~9)?\n")) - 1

        # Execute second move
        clear_output(wait=False)
        time.sleep(1)
        current_state[second_move] = "O"
        row = self.ai.df_2.index[(self.ai.df_2[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(2, row)

        # AI third move
        row = self.ai.third_move(row)
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_3.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(3, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(3, row)
        time.sleep(1)

        # Ask fourth move
        fourth_move = int(input("Your second move(1~9)?\n")) - 1
        while (fourth_move not in range(9)) or (current_state[fourth_move] != " "):
            fourth_move = int(input("Invalid input...\nYour second move(1~9)?\n")) - 1

        # Execute fourth move
        clear_output(wait=False)
        time.sleep(1)
        current_state[fourth_move] = "O"
        row = self.ai.df_4.index[(self.ai.df_4[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(4, row)

        # AI fifth move
        row = self.ai.fifth_move(row)
        time.sleep(1)  # Fake thinking
        current_state = self.ai.df_5.loc[row, range(9)]
        clear_output(wait=False)
        self.ai.display_board(5, row)
        time.sleep(0.1)  # Blink effect as notification
        clear_output(wait=False)
        self.ai.display_board(5, row)
        if self.ai.is_game_over(5, row):
            print("You lose!\n")
            return
        time.sleep(1)

        # Ask sixth move
        sixth_move = int(input("Your third move(1~9)?\n")) - 1
        while (sixth_move not in range(9)) or (current_state[sixth_move] != " "):
            sixth_move = int(input("Invalid input...\nYour third move(1~9)?\n")) - 1

        # Execute sixth move
        clear_output(wait=False)
        time.sleep(1)
        current_state[sixth_move] = "O"
        row = self.ai.df_6.index[(self.ai.df_6[range(9)] == current_state).all(axis=1)][0]
        self.ai.display_board(6, row)
        if self.ai.is_game_over(6, row):  # test for winning
            print("You win!\n")
            return

        # Now moving instead of adding
        while True:
            # AI move
            row = self.ai.further_move(row, "X")
            time.sleep(1)  # Fak thinking
            current_state = self.ai.df_6.loc[row, range(9)]
            clear_output(wait=False)
            self.ai.display_board(6, row)
            time.sleep(0.1)  # Blink effect as notification
            clear_output(wait=False)
            self.ai.display_board(6, row)
            if self.ai.is_game_over(6, row):
                print("You lose!\n")
                return
            time.sleep(1)

            # Ask human move
            remove = int(input("Remove your marker from (1~9)?\n")) - 1
            while (remove not in range(9)) or (current_state[remove] != "O"):
                remove = int(input("Invalid input...\nRemove your marker from (1~9)?\n")) - 1
            locate = int(input("Relocate your marker into (1~9)?\n")) - 1
            while (locate not in range(9)) or (current_state[locate] != " "):
                locate = int(input("Invalid input...\nRelocate your marker into (1~9)?\n")) - 1

            # Execute human move
            clear_output(wait=False)
            time.sleep(1)
            current_state[remove] = " "
            current_state[locate] = "O"
            row = self.ai.df_6.index[(self.ai.df_6[range(9)] == current_state).all(axis=1)][0]
            self.ai.display_board(6, row)
            if self.ai.is_game_over(6, row):
                print("You win!\n")
                break
        return

