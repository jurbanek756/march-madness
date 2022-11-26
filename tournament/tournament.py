#!/usr/bin/env python3

import logging
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
        log_results=True,
    ):
        self.log_results = log_results
        if self.log_results:
            logging.basicConfig(
                encoding="UTF-8",
                level="INFO",
                handlers=[
                    logging.FileHandler("NCAA_Tournament_Results.txt"),
                    logging.StreamHandler(),
                ],
                format="%(message)s",
            )
        self.play_in_rank = play_in_rank
        self.predict = prediction_method
        self.west = Group(west, self.predict, self.play_in_rank, log_results)
        self.south = Group(south, self.predict, self.play_in_rank, log_results)
        self.east = Group(east, self.predict, self.play_in_rank, log_results)
        self.midwest = Group(midwest, self.predict, self.play_in_rank, log_results)
        self.west_winner = None
        self.east_winner = None
        self.south_winner = None
        self.midwest_winner = None

    def run(self):
        west_winner, east_winner, south_winner, midwest_winner = self.group_winners()
        tournament_winner = self.tournament_winner(
            west_winner, east_winner, south_winner, midwest_winner
        )
        if self.log_results:
            logging.info("NCAA Champions: %s", tournament_winner)
        return tournament_winner

    def group_winners(self):
        self.first_four()
        (
            west_first_round,
            east_first_round,
            south_first_round,
            midwest_first_round,
        ) = self.first_round()
        (
            west_second_round,
            east_second_round,
            south_second_round,
            midwest_second_round,
        ) = self.second_round(
            west_first_round, east_first_round, south_first_round, midwest_first_round
        )

        (
            west_sweet_sixteen,
            east_sweet_sixteen,
            south_sweet_sixteen,
            midwest_sweet_sixteen,
        ) = self.sweet_sixteen(
            west_first_round, east_first_round, south_first_round, midwest_first_round
        )

        return self.elite_eight(
            west_sweet_sixteen,
            east_sweet_sixteen,
            south_sweet_sixteen,
            midwest_sweet_sixteen,
        )

    def tournament_winner(self, west_winner, east_winner, south_winner, midwest_winner):
        left = self.predict(west_winner, east_winner)
        right = self.predict(south_winner, midwest_winner)
        if self.log_results:
            logging.info("Championship Game: %s vs. %s", left, right)
        return self.predict(left, right)

    def first_four(self):
        west_first_four = self.west.first_four()
        if self.log_results:
            logging.info("West First Four Winner: %s", west_first_four)

        east_first_four = self.east.first_four()
        if self.log_results:
            logging.info("East First Four Winner: %s", east_first_four)

        south_first_four = self.south.first_four()
        if self.log_results:
            logging.info("South First Four Winner: %s", south_first_four)

        midwest_first_four = self.midwest.first_four()
        if self.log_results:
            logging.info("Midwest First Four Winner: %s", midwest_first_four)

        return west_first_four, east_first_four, south_first_four, midwest_first_four

    def first_round(self):
        west_first_round = self.west.first_round()
        if self.log_results:
            logging.info("West First Round Results:")
            logging.info(west_first_round)

        east_first_round = self.east.first_round()
        if self.log_results:
            logging.info("East First Round Results:")
            logging.info(east_first_round)

        south_first_round = self.south.first_round()
        if self.log_results:
            logging.info("South First Round Results:")
            logging.info(south_first_round)

        midwest_first_round = self.midwest.first_round()
        if self.log_results:
            logging.info("Midwest First Round Results:")
            logging.info(midwest_first_round)

        return (
            west_first_round,
            east_first_round,
            south_first_round,
            midwest_first_round,
        )

    def second_round(
        self, west_first_round, east_first_round, south_first_round, midwest_first_round
    ):
        west_second_round = self.west.second_round(west_first_round)
        if self.log_results:
            logging.info("West Second Round Results:")
            logging.info(west_second_round)

        east_second_round = self.east.second_round(east_first_round)
        if self.log_results:
            logging.info("East Second Round Results:")
            logging.info(east_second_round)

        south_second_round = self.south.second_round(south_first_round)
        if self.log_results:
            logging.info("South Second Round Results:")
            logging.info(south_second_round)

        midwest_second_round = self.midwest.second_round(midwest_first_round)
        if self.log_results:
            logging.info("Midwest Second Round Results:")
            logging.info(midwest_second_round)

        return (
            west_second_round,
            east_second_round,
            south_second_round,
            midwest_second_round,
        )

    def sweet_sixteen(
        self,
        west_second_round,
        east_second_round,
        south_second_round,
        midwest_second_round,
    ):
        west_sweet_sixteen = self.west.sweet_sixteen(west_second_round)
        if self.log_results:
            logging.info("West Sweet Sixteen Results:")
            logging.info(west_sweet_sixteen)

        east_sweet_sixteen = self.east.sweet_sixteen(east_second_round)
        if self.log_results:
            logging.info("East Sweet Sixteen Results:")
            logging.info(east_sweet_sixteen)

        south_sweet_sixteen = self.south.sweet_sixteen(south_second_round)
        if self.log_results:
            logging.info("South Sweet Sixteen Results:")
            logging.info(south_sweet_sixteen)

        midwest_sweet_sixteen = self.midwest.sweet_sixteen(midwest_second_round)
        if self.log_results:
            logging.info("Midwest Sweet Sixteen Results:")
            logging.info(midwest_sweet_sixteen)

        return (
            west_sweet_sixteen,
            east_sweet_sixteen,
            south_sweet_sixteen,
            midwest_sweet_sixteen,
        )

    def elite_eight(
        self,
        west_sweet_sixteen,
        east_sweet_sixteen,
        south_sweet_sixteen,
        midwest_sweet_sixteen,
    ):
        west_winner = self.west.elite_eight(west_sweet_sixteen)
        if self.log_results:
            logging.info(f"West Group Winner: {west_winner}")

        east_winner = self.east.elite_eight(east_sweet_sixteen)
        if self.log_results:
            logging.info(f"East Group Winner: {east_winner}")

        south_winner = self.south.elite_eight(south_sweet_sixteen)
        if self.log_results:
            logging.info(f"South Group Winner: {south_winner}")

        midwest_winner = self.midwest.elite_eight(midwest_sweet_sixteen)
        if self.log_results:
            logging.info(f"Midwest Group Winner: {midwest_winner}")

        return west_winner, east_winner, south_winner, midwest_winner


class Group:
    def __init__(self, ranking_dict, prediction_method, play_in_rank, log_results=True):
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
        self.log_results = log_results
        if self.log_results:
            logging.info("Group Rankings:")
            logging.info(self.ranking_dict)
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
        self.ranking_dict[self.play_in_rank] = self.predict(
            self.play_in, self.ranking_dict[self.play_in_rank]
        )
        return self.ranking_dict[self.play_in_rank]

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
            "1_8": self.predict(
                first_round_results["1_16"], first_round_results["8_9"]
            ),
            "2_7": self.predict(
                first_round_results["2_15"], first_round_results["7_10"]
            ),
            "3_6": self.predict(
                first_round_results["3_14"], first_round_results["6_11"]
            ),
            "4_5": self.predict(
                first_round_results["4_13"], first_round_results["5_12"]
            ),
        }

    def sweet_sixteen(self, second_round_results):
        return {
            "1_4": self.predict(
                second_round_results["1_8"], second_round_results["4_5"]
            ),
            "2_3": self.predict(
                second_round_results["2_7"], second_round_results["3_6"]
            ),
        }

    def elite_eight(self, sweet_sixteen_results):
        return self.predict(sweet_sixteen_results["1_4"], sweet_sixteen_results["2_3"])
