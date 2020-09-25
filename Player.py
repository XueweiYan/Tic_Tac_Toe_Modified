import os
import numpy as np
import pandas as pd
from random import random
from sympy.utilities.iterables import multiset_permutations as perm


class Player:

    def __init__(self, database=None):
        self._valid_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self._alpha = 0.5  # Learn rate
        self._delta_epsilon = 0.00000001
        self._min_epsilon = 0.01
        self._consider_win = 0.9999  # Meaning the state almost guarantees a winning, no need to explore
        if database is None:
            self._epsilon = 0.5  # Explore rate
            self.df_6 = self.initializedf_6()
            self.df_5 = self.initializedf_5()
            self.df_4 = self.initializedf_4()
            self.df_3 = self.initializedf_3()
            self.df_2 = self.initializedf_2()
            self.df_1 = self.initializedf_1()
            self.df_0 = self.initializedf_0()
        else:
            self._epsilon = 0.0
            self.df_6 = pd.read_csv(database + "/df_6.csv").rename(columns={str(x): x for x in range(9)})
            self.df_6["successor_X"] = self.df_6["successor_X"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])
            self.df_6["successor_O"] = self.df_6["successor_O"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_5 = pd.read_csv(database + "/df_5.csv").rename(columns={str(x): x for x in range(9)})
            self.df_5["successor_O"] = self.df_5["successor_O"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_4 = pd.read_csv(database + "/df_4.csv").rename(columns={str(x): x for x in range(9)})
            self.df_4["successor_X"] = self.df_4["successor_X"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_3 = pd.read_csv(database + "/df_3.csv").rename(columns={str(x): x for x in range(9)})
            self.df_3["successor_O"] = self.df_3["successor_O"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_2 = pd.read_csv(database + "/df_2.csv").rename(columns={str(x): x for x in range(9)})
            self.df_2["successor_X"] = self.df_2["successor_X"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_1 = pd.read_csv(database + "/df_1.csv").rename(columns={str(x): x for x in range(9)})
            self.df_1["successor_O"] = self.df_1["successor_O"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

            self.df_0 = pd.read_csv(database + "/df_0.csv").rename(columns={str(x): x for x in range(9)})
            self.df_0["successor_X"] = self.df_0["successor_X"].apply(lambda x: [int(y) for y in x[1:-1].split(",")])

    def initialize_reward(self, row):
        X_win = row.index[row == 'X'].tolist() in self._valid_lines
        O_win = row.index[row == 'O'].tolist() in self._valid_lines
        if X_win and O_win:
            return 101  # A customized error code to mark impossible situations
        return 1 * X_win + (-1) * O_win  # 1 for player X winning, -1 for player O, 0 for none.

    def initializedf_6(self):
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

    def initializedf_5(self):
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

    def initializedf_4(self):
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

    def initializedf_3(self):
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

    def initializedf_2(self):
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

    def initializedf_1(self):
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

    def initializedf_0(self):
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
        if (random() < self._epsilon) and (max_reward_X < self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_0.loc[0, "reward_X"] = (
                    self.df_0.loc[0, "reward_X"] +
                    self._alpha * (max_reward_X - self.df_0.loc[0, "reward_X"])
            )
            return decision[0]

    def second_move(self, prev_decision):
        successors = self.df_1.loc[prev_decision, "successor_O"]
        options = self.df_2.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self._epsilon) and (min_reward_X > -self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_1.loc[prev_decision, "reward_X"] = (
                    self.df_1.loc[prev_decision, "reward_X"] +
                    self._alpha * (min_reward_X - self.df_1.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def third_move(self, prev_decision):
        successors = self.df_2.loc[prev_decision, "successor_X"]
        options = self.df_3.loc[successors]
        max_reward_X = options["reward_X"].max()
        if (random() < self._epsilon) and (max_reward_X < self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_2.loc[prev_decision, "reward_X"] = (
                    self.df_2.loc[prev_decision, "reward_X"] +
                    self._alpha * (max_reward_X - self.df_2.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def fourth_move(self, prev_decision):
        successors = self.df_3.loc[prev_decision, "successor_O"]
        options = self.df_4.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self._epsilon) and (min_reward_X > -self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_3.loc[prev_decision, "reward_X"] = (
                    self.df_3.loc[prev_decision, "reward_X"] +
                    self._alpha * (min_reward_X - self.df_3.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def fifth_move(self, prev_decision):
        successors = self.df_4.loc[prev_decision, "successor_X"]
        options = self.df_5.loc[successors]
        max_reward_X = options["reward_X"].max()
        if (random() < self._epsilon) and (max_reward_X < self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
            self.df_4.loc[prev_decision, "reward_X"] = (
                    self.df_4.loc[prev_decision, "reward_X"] +
                    self._alpha * (max_reward_X - self.df_4.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def sixth_move(self, prev_decision):
        successors = self.df_5.loc[prev_decision, "successor_O"]
        options = self.df_6.loc[successors]
        min_reward_X = options["reward_X"].min()
        if (random() < self._epsilon) and (min_reward_X > -self._consider_win):  # Explore move
            self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
            return options.sample(n=1).index[0]
        else:  # Exploit move
            decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
            self.df_5.loc[prev_decision, "reward_X"] = (
                    self.df_5.loc[prev_decision, "reward_X"] +
                    self._alpha * (min_reward_X - self.df_5.loc[prev_decision, "reward_X"])
            )
            return decision[0]

    def further_move(self, prev_decision, cur_player):
        if cur_player == "X":
            successors = self.df_6.loc[prev_decision, "successor_X"]
            options = self.df_6.loc[successors]
            max_reward_X = options["reward_X"].max()
            if (random() < self._epsilon) and (max_reward_X < self._consider_win):  # Explore move
                self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
                return options.sample(n=1).index[0]
            else:  # Exploit move
                decision = options.loc[options["reward_X"] == max_reward_X].sample(n=1).index
                self.df_6.loc[prev_decision, "reward_X"] = (
                        self.df_6.loc[prev_decision, "reward_X"] +
                        self._alpha * (max_reward_X - self.df_6.loc[prev_decision, "reward_X"])
                )
                return decision[0]
        else:
            successors = self.df_6.loc[prev_decision, "successor_O"]
            options = self.df_6.loc[successors]
            min_reward_X = options["reward_X"].min()
            if (random() < self._epsilon) and (min_reward_X > -self._consider_win):  # Explore move
                self._epsilon = max(self._epsilon - self._delta_epsilon, self._min_epsilon)
                return options.sample(n=1).index[0]
            else:  # Exploit move
                decision = options.loc[options["reward_X"] == min_reward_X].sample(n=1).index
                self.df_6.loc[prev_decision, "reward_X"] = (
                        self.df_6.loc[prev_decision, "reward_X"] +
                        self._alpha * (min_reward_X - self.df_6.loc[prev_decision, "reward_X"])
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
        output = row.loc[range(9)]
        for box in range(9):
            if output[box] == " ":
                output[box] = "-" + str(box + 1) + "-"
            else:
                output[box] = " " + output[box] + " "
        print(" —————————")
        print("|", output[0], "|", output[1], "|", output[2], "|")
        print(" —————————")
        print("|", output[3], "|", output[4], "|", output[5], "|")
        print(" —————————")
        print("|", output[6], "|", output[7], "|", output[8], "|")
        print(" —————————")

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

    def save_dfs(self, database):
        if not os.path.exists(database):
            os.mkdir(database)
        self.df_6.to_csv(database + "/df_6.csv", index=False)
        self.df_5.to_csv(database + "/df_5.csv", index=False)
        self.df_4.to_csv(database + "/df_4.csv", index=False)
        self.df_3.to_csv(database + "/df_3.csv", index=False)
        self.df_2.to_csv(database + "/df_2.csv", index=False)
        self.df_1.to_csv(database + "/df_1.csv", index=False)
        self.df_0.to_csv(database + "/df_0.csv", index=False)

    def set_epsilon(self, epsilon):
        self._epsilon = epsilon

    def set_alpha(self, alpha):
        self._alpha = alpha