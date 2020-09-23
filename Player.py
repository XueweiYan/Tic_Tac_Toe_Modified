import numpy as np
import pandas as pd
from random import random
from sympy.utilities.iterables import multiset_permutations as perm


class Player:

    def __init__(self):
        self.valid_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.alpha = 0.3  # Learn rate
        self.epsilon = 0.5  # Explore rate
        self.consider_win = 0.9999  # Meaning the state almost guarantees a winning, no need to explore
        self.df_6 = self.initialize_df_6()
        self.df_5 = self.initialize_df_5()
        self.df_4 = self.initialize_df_4()
        self.df_3 = self.initialize_df_3()
        self.df_2 = self.initialize_df_2()
        self.df_1 = self.initialize_df_1()
        self.df_0 = self.initialize_df_0()

    def initialize_reward(self, row):
        X_win = row.index[row == 'X'].tolist() in self.valid_lines
        O_win = row.index[row == 'O'].tolist() in self.valid_lines
        if X_win and O_win:
            return 101  # A customized error code to mark impossible situations
        return 1 * X_win + (-1) * O_win  # 1 for player X winning, -1 for player O, 0 for none.

    def initialize_df_6(self):
        def find_successor_X(row):
            O_same = (
                df_6.loc[(df_6[row.index[row == 'O']] == 'O').all(axis=1)]
                    .drop(columns=["reward_X"])
            )
            diff_count = (O_same != (row.drop(["reward_X"]))).sum(axis=1)
            return diff_count.index[diff_count == 2].tolist()

        def find_successor_O(row):
            X_same = (
                df_6.loc[(df_6[row.index[row == 'X']] == 'X').all(axis=1)]
                    .drop(columns=["reward_X", "successor_X"])
            )
            diff_count = (X_same != row.drop(["reward_X", "successor_X"])).sum(axis=1)
            return diff_count.index[diff_count == 2].tolist()

        six_marks = np.array([' ', ' ', ' ', 'X', 'X', 'X', 'O', 'O', 'O'])
        df_6 = pd.DataFrame(list(perm(six_marks)))
        df_6["reward_X"] = df_6.apply(self.initialize_reward, axis=1)
        df_6 = df_6.loc[df_6["reward_X"] != 101].reset_index(
            drop=True)  # Remove all impossible cases identified in function initialize_ward
        df_6["successor_X"] = df_6.apply(find_successor_X, axis=1)
        df_6["successor_O"] = df_6.apply(find_successor_O, axis=1)
        df_6["game_over"] = df_6["reward_X"] != 0

        return df_6

    def initialize_df_5(self):
        def find_successor_O(row):
            df_6_states = self.df_6.drop(columns=["reward_X", "successor_X", "successor_O", "game_over"])
            diff_count = (df_6_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        five_marks = np.array([' ', ' ', ' ', ' ', 'X', 'X', 'X', 'O', 'O'])
        df_5 = pd.DataFrame(list(perm(five_marks)))
        df_5["reward_X"] = df_5.apply(self.initialize_reward, axis=1)
        # Remove all impossible cases identified in function initialize_ward
        df_5 = df_5.loc[df_5["reward_X"] != 101].reset_index(drop=True)
        df_5["successor_O"] = df_5.apply(find_successor_O, axis=1)
        df_5["game_over"] = df_5["reward_X"] != 0

        return df_5

    def initialize_df_4(self):
        def find_successor_X(row):
            df_5_states = self.df_5.drop(columns=["reward_X", "successor_O", "game_over"])
            diff_count = (df_5_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        four_marks = np.array([' ', ' ', ' ', ' ', ' ', 'X', 'X', 'O', 'O'])
        df_4 = pd.DataFrame(list(perm(four_marks)))
        df_4["reward_X"] = 0  # Impossible to win with at most two marks for each player
        df_4["successor_X"] = df_4.apply(find_successor_X, axis=1)
        df_4["game_over"] = False  # Impossible to have a game over state with first four hands

        return df_4

    def initialize_df_3(self):
        def find_successor_O(row):
            df_4_states = self.df_4.drop(columns=["reward_X", "successor_X", "game_over"])
            diff_count = (df_4_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        three_marks = np.array([' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'O'])
        df_3 = pd.DataFrame(list(perm(three_marks)))
        df_3["reward_X"] = 0  # Impossible to win with at most two marks for each player
        df_3["successor_O"] = df_3.apply(find_successor_O, axis=1)
        df_3["game_over"] = False  # Impossible to have a game over state with first three hands

        return df_3

    def initialize_df_2(self):
        def find_successor_X(row):
            df_3_states = self.df_3.drop(columns=["reward_X", "successor_O", "game_over"])
            diff_count = (df_3_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        two_marks = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'O'])
        df_2 = pd.DataFrame(list(perm(two_marks)))
        df_2["reward_X"] = 0  # Impossible to win with at most two marks for each player
        df_2["successor_X"] = df_2.apply(find_successor_X, axis=1)
        df_2["game_over"] = False  # Impossible to have a game over state with first two hands

        return df_2

    def initialize_df_1(self):
        def find_successor_O(row):
            df_2_states = self.df_2.drop(columns=["reward_X", "successor_X", "game_over"])
            diff_count = (df_2_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        one_marks = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'])
        df_1 = pd.DataFrame(list(perm(one_marks)))
        df_1["reward_X"] = 0  # Impossible to win with at most two marks for each player
        df_1["successor_O"] = df_1.apply(find_successor_O, axis=1)
        df_1["game_over"] = False  # Impossible to have a game over state with the first hand

        return df_1

    def initialize_df_0(self):
        def find_successor_X(row):
            df_1_states = self.df_1.drop(columns=["reward_X", "successor_O", "game_over"])
            diff_count = (df_1_states != row.drop(["reward_X"])).sum(axis=1)
            return diff_count.index[diff_count == 1].tolist()

        no_marks = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
        df_0 = pd.DataFrame(list(perm(no_marks)))
        df_0["reward_X"] = 0  # Impossible to win with at most two marks for each player
        df_0["successor_X"] = df_0.apply(find_successor_X, axis=1)
        df_0["game_over"] = False  # Impossible to have a game over state with no marks

        return df_0

    """
    Below is the methods for RL learning algorithm.
    """

    def start_new_game(self):
        successors = self.df_0.loc[0, "successor_X"]
        options = self.df_1.loc[successors]
        max_reward_X = options["reward_X"].max()
        if (random() < self.epsilon) and (max_reward_X < self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_0.loc[0, "reward_X"] = (
                    self.df_0.loc[0, "reward_X"] +
                    self.alpha * (max_reward_X - self.df_0.loc[0, "reward_X"])
            )
            return decision[0]

    def second_move(self, prev_decision):
        successors = self.df_1.loc[prev_decision, "successor_O"]
        options = self.df_2.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self.epsilon) and (min_reward_X > -self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_1.loc[prev_decision, "reward_X"] = (
                    self.df_1.loc[prev_decision, "reward_X"] +
                    self.alpha * (min_reward_X - self.df_1.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def third_move(self, prev_decision):
        successors = self.df_2.loc[prev_decision, "successor_X"]
        options = self.df_3.loc[successors]
        max_reward_X = options["reward_X"].max()
        if (random() < self.epsilon) and (max_reward_X < self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_2.loc[prev_decision, "reward_X"] = (
                    self.df_2.loc[prev_decision, "reward_X"] +
                    self.alpha * (max_reward_X - self.df_2.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def fourth_move(self, prev_decision):
        successors = self.df_3.loc[prev_decision, "successor_O"]
        options = self.df_4.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self.epsilon) and (min_reward_X > -self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_3.loc[prev_decision, "reward_X"] = (
                    self.df_3.loc[prev_decision, "reward_X"] +
                    self.alpha * (min_reward_X - self.df_3.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def fifth_move(self, prev_decision):
        successors = self.df_4.loc[prev_decision, "successor_X"]
        options = self.df_5.loc[successors]
        max_reward_X = options["reward_X"].max()
        if (random() < self.epsilon) and (max_reward_X < self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_4.loc[prev_decision, "reward_X"] = (
                    self.df_4.loc[prev_decision, "reward_X"] +
                    self.alpha * (max_reward_X - self.df_4.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def sixth_move(self, prev_decision):
        successors = self.df_5.loc[prev_decision, "successor_O"]
        options = self.df_6.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self.epsilon) and (min_reward_X > -self.consider_win):  # Explore move
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_5.loc[prev_decision, "reward_X"] = (
                    self.df_5.loc[prev_decision, "reward_X"] +
                    self.alpha * (min_reward_X - self.df_5.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def further_move(self, prev_decision, cur_player):
        if cur_player == "X":
            successors = self.df_6.loc[prev_decision, "successor_X"]
            options = self.df_6.loc[successors]
            max_reward_X = options["reward_X"].max()
            if (random() < self.epsilon) and (max_reward_X < self.consider_win):  # Explore move
                return options.sample(n=1).index[0]
            else:  # Exploit move
                decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
                self.df_6.loc[prev_decision, "reward_X"] = (
                        self.df_6.loc[prev_decision, "reward_X"] +
                        self.alpha * (max_reward_X - self.df_6.loc[prev_decision, "reward_X"])
                )
                return decision[0]
        else:
            successors = self.df_6.loc[prev_decision, "successor_O"]
            options = self.df_6.loc[successors]
            min_reward_X = options["reward_X"].min()
            if (random() < self.epsilon) and (min_reward_X > -self.consider_win):  # Explore move
                return options.sample(n=1).index[0]
            else:  # Exploit move
                decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
                self.df_6.loc[prev_decision, "reward_X"] = (
                        self.df_6.loc[prev_decision, "reward_X"] +
                        self.alpha * (min_reward_X - self.df_6.loc[prev_decision, "reward_X"])
                )
                return decision[0]

    def is_game_over(self, df_num, row):
        if df_num == 5:
            return self.df_5.loc[row, "game_over"]
        elif df_num == 6:
            return self.df_6.loc[row, "game_over"]
        else:
            return False

    def beautify_board(self, row):
        print(row[0], row[1], row[2], "\n")
        print(row[3], row[4], row[5], "\n")
        print(row[6], row[7], row[8], "\n")

    def display_board(self, df_num, row):
        if df_num == 0:
            self.beautify_board(self.df_0.loc[row])
        elif df_num == 1:
            self.beautify_board(self.df_1.loc[row])
        elif df_num == 2:
            self.beautify_board(self.df_2.loc[row])
        elif df_num == 3:
            self.beautify_board(self.df_3.loc[row])
        elif df_num == 4:
            self.beautify_board(self.df_4.loc[row])
        elif df_num == 5:
            self.beautify_board(self.df_5.loc[row])
        else:
            self.beautify_board(self.df_6.loc[row])

