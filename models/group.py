from collections import OrderedDict


class Group:
    def __init__(
        self,
        ranking_dict,
        prediction_method,
        prediction_method_kwargs,
        play_in_rank,
        group_name=None,
    ):
        self.one = ranking_dict[1]
        self.two = ranking_dict[2]
        self.three = ranking_dict[3]
        self.four = ranking_dict[4]
        self.five = ranking_dict[5]
        self.six = ranking_dict[6]
        self.seven = ranking_dict[7]
        self.eight = ranking_dict[8]
        self.nine = ranking_dict[9]
        self.ten = ranking_dict[10]
        self.eleven = ranking_dict[11]
        self.twelve = ranking_dict[12]
        self.thirteen = ranking_dict[13]
        self.fourteen = ranking_dict[14]
        self.fifteen = ranking_dict[15]
        self.sixteen = ranking_dict[16]
        self.play_in = ranking_dict["play_in"]
        self.predict = prediction_method
        self.prediction_method_kwargs = prediction_method_kwargs
        self.play_in_rank = play_in_rank
        self.group_name = group_name
        self.play_in.tournament_rank = self.play_in_rank
        self.first_four_results = None
        self.first_round_results = None
        self.second_round_results = None
        self.sweet_sixteen_results = None
        self.group_winner = None

    @property
    def ranking_dict(self):
        return {
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine,
            10: self.ten,
            11: self.eleven,
            12: self.twelve,
            13: self.thirteen,
            14: self.fourteen,
            15: self.fifteen,
            16: self.sixteen,
            "Play In": self.play_in,
        }

    def first_four(self):
        first_four_winner = self.predict(
            self.play_in,
            self.ranking_dict[self.play_in_rank],
            group_name=self.group_name,
            round_name="First Four",
            **self.prediction_method_kwargs,
        )
        if self.play_in_rank == 16:
            self.sixteen = first_four_winner
        elif self.play_in_rank == 15:
            self.fifteen = first_four_winner
        elif self.play_in_rank == 14:
            self.fourteen = first_four_winner
        elif self.play_in_rank == 13:
            self.thirteen = first_four_winner
        elif self.play_in_rank == 12:
            self.twelve = first_four_winner
        elif self.play_in_rank == 11:
            self.eleven = first_four_winner
        elif self.play_in_rank == 10:
            self.ten = first_four_winner
        else:
            raise ValueError("Unhandled play-in rank")
        return self.ranking_dict[self.play_in_rank]

    def first_round(self):
        return OrderedDict(
            {
                "1_16": self.predict(
                    self.one,
                    self.sixteen,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "8_9": self.predict(
                    self.eight,
                    self.nine,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "5_12": self.predict(
                    self.five,
                    self.twelve,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "4_13": self.predict(
                    self.four,
                    self.thirteen,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "6_11": self.predict(
                    self.six,
                    self.eleven,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "3_14": self.predict(
                    self.three,
                    self.fourteen,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "7_10": self.predict(
                    self.seven,
                    self.ten,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
                "2_15": self.predict(
                    self.two,
                    self.fifteen,
                    group_name=self.group_name,
                    round_name="First Round",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def second_round(self, first_round_results):
        return OrderedDict(
            {
                "1_8": self.predict(
                    first_round_results["1_16"],
                    first_round_results["8_9"],
                    group_name=self.group_name,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "4_5": self.predict(
                    first_round_results["4_13"],
                    first_round_results["5_12"],
                    group_name=self.group_name,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "3_6": self.predict(
                    first_round_results["3_14"],
                    first_round_results["6_11"],
                    group_name=self.group_name,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
                "2_7": self.predict(
                    first_round_results["2_15"],
                    first_round_results["7_10"],
                    group_name=self.group_name,
                    round_name="Second Round",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def sweet_sixteen(self, second_round_results):
        return OrderedDict(
            {
                "1_4": self.predict(
                    second_round_results["1_8"],
                    second_round_results["4_5"],
                    group_name=self.group_name,
                    round_name="Sweet Sixteen",
                    **self.prediction_method_kwargs,
                ),
                "2_3": self.predict(
                    second_round_results["2_7"],
                    second_round_results["3_6"],
                    group_name=self.group_name,
                    round_name="Sweet Sixteen",
                    **self.prediction_method_kwargs,
                ),
            }
        )

    def elite_eight(self, sweet_sixteen_results):
        return self.predict(
            sweet_sixteen_results["1_4"],
            sweet_sixteen_results["2_3"],
            group_name=self.group_name,
            round_name="Elite Eight",
            **self.prediction_method_kwargs,
        )
