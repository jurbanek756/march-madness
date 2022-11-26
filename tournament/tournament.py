from predict.select_team import weighted_random_selection


class Tournament:
    def __init__(
        self,
        west,
        south,
        east,
        midwest,
        play_in_rank,
        prediction_method=weighted_random_selection,
    ):
        self.play_in_rank = play_in_rank
        self.predict = prediction_method
        self.west = Group(west, self.predict, self.play_in_rank)
        self.south = Group(south, self.predict, self.play_in_rank)
        self.east = Group(east, self.predict, self.play_in_rank)
        self.midwest = Group(midwest, self.predict, self.play_in_rank)


class Group:
    def __init__(self, ranking_dict, prediction_method, play_in_rank):
        self.one = ranking_dict["one"]
        self.two = ranking_dict["two"]
        self.three = ranking_dict["three"]
        self.four = ranking_dict["four"]
        self.five = ranking_dict["five"]
        self.six = ranking_dict["six"]
        self.seven = ranking_dict["seven"]
        self.eight = ranking_dict["eight"]
        self.nine = ranking_dict["nine"]
        self.ten = ranking_dict["ten"]
        self.eleven = ranking_dict["eleven"]
        self.twelve = ranking_dict["twelve"]
        self.thirteen = ranking_dict["thirteen"]
        self.fourteen = ranking_dict["fourteen"]
        self.fifteen = ranking_dict["fifteen"]
        self.sixteen = ranking_dict["sixteen"]
        self.play_in = ranking_dict["play_in"]
        self.predict = prediction_method
        self.play_in_rank = play_in_rank
        self.group_winner = self.run()

    def run(self):
        self.first_four()
        first_round_results = self.first_round()
        second_round_results = self.second_round(first_round_results)
        sweet_sixteen_results = self.sweet_sixteen(second_round_results)
        return self.elite_eight(sweet_sixteen_results)

    def first_four(self):
        ranking_dict = {
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
        }
        ranking_dict[self.play_in_rank] = self.predict(
            self.play_in, ranking_dict[self.play_in_rank]
        )

    def first_round(self):
        return {
            "1_16": self.predict(self.one, self.sixteen),
            "2_15": self.predict(self.two, self.fifteen),
            "3_14": self.predict(self.three, self.fourteen),
            "4_13": self.predict(self.four, self.thirteen),
            "5_12": self.predict(self.five, self.twelve),
            "6_11": self.predict(self.six, self.eleven),
            "7_10": self.predict(self.seven, self.ten),
            "8_9": self.predict(self.eight, self.nine),
        }

    def second_round(self, first_round_results):
        return {
            "1_8": self.predict(first_round_results["1_16"], first_round_results["8_9"]),
            "2_7": self.predict(first_round_results["2_15"], first_round_results["7_10"]),
            "3_6": self.predict(first_round_results["3_14"], first_round_results["6_11"]),
            "4_5": self.predict(first_round_results["4_13"], first_round_results["5_12"]),
        }

    def sweet_sixteen(self, second_round_results):
        return {
            "1_4": self.predict(second_round_results["1_8"], second_round_results["4_5"]),
            "2_3": self.predict(second_round_results["2_7"], second_round_results["3_6"]),
        }

    def elite_eight(self, sweet_sixteen_results):
        return self.predict(sweet_sixteen_results["1_4"], sweet_sixteen_results["2_3"])
