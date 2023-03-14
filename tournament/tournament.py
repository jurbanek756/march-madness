#!/usr/bin/env python3

import json
import logging
from predict.select_team import weighted_random_selection


class Tournament:
    def __init__(
        self,
        left_top,
        left_bottom,
        right_top,
        right_bottom,
        left_top_play_in_rank,
        left_bottom_play_in_rank,
        right_top_play_in_rank,
        right_bottom_play_in_rank,
        prediction_method=weighted_random_selection,
        log_results=True,
    ):
        self.log_results = log_results
        if self.log_results:
            logging.basicConfig(
                encoding="UTF-8",
                level="INFO",
                handlers=[
                    logging.FileHandler("NCAA_Tournament_Results.log"),
                    logging.StreamHandler(),
                ],
                format="%(message)s",
            )
        self.predict = prediction_method
        self.left_top = Group(left_top, self.predict, left_top_play_in_rank)
        self.left_bottom = Group(left_bottom, self.predict, left_bottom_play_in_rank)
        self.right_top = Group(right_top, self.predict, right_top_play_in_rank)
        self.right_bottom = Group(right_bottom, self.predict, right_bottom_play_in_rank)
        self.left_top_winner = None
        self.left_bottom_winner = None
        self.right_top_winner = None
        self.right_bottom_winner = None

    def run(self):
        if self.log_results:
            logging.info("Left Top Group Rankings:")
            logging.info(json.dumps(self.left_top.ranking_dict, default=str, indent=2))
            logging.info("Left Bottom Group Rankings:")
            logging.info(
                json.dumps(self.left_bottom.ranking_dict, default=str, indent=2)
            )
            logging.info("Right Top Group Rankings:")
            logging.info(json.dumps(self.right_top.ranking_dict, default=str, indent=2))
            logging.info("Right Bottom Group Rankings:")
            logging.info(
                json.dumps(self.right_bottom.ranking_dict, default=str, indent=2)
            )
        west_winner, east_winner, south_winner, midwest_winner = self.group_winners()
        tournament_winner = self.tournament_winner(
            south_winner, east_winner, midwest_winner, west_winner
        )
        if self.log_results:
            logging.info("NCAA Champions: %s", tournament_winner)
        return tournament_winner

    def group_winners(self):
        self.first_four()
        (
            lt_r1,
            lb_r1,
            rt_r1,
            rb_r1,
        ) = self.first_round()
        lt_r2, lb_r2, rt_r2, rb_r2 = self.second_round(lt_r1, lb_r1, rt_r1, rb_r1)
        (
            lt_sweet_sixteen,
            lb_sweet_sixteen,
            rt_sweet_sixteen,
            rb_sweet_sixteen,
        ) = self.sweet_sixteen(lt_r2, lb_r2, rt_r2, rb_r2)

        return self.elite_eight(
            lt_sweet_sixteen,
            lb_sweet_sixteen,
            rt_sweet_sixteen,
            rb_sweet_sixteen,
        )

    def tournament_winner(self, left_top, left_bottom, right_top, right_bottom):
        left = self.predict(left_top, left_bottom)
        right = self.predict(right_top, right_bottom)
        if self.log_results:
            logging.info("Championship Game: %s vs. %s", left, right)
        return self.predict(left, right)

    def first_four(self):
        west_first_four = self.left_top.first_four()
        if self.log_results:
            logging.info("Left Top First Four Winner: %s", west_first_four)

        east_first_four = self.left_bottom.first_four()
        if self.log_results:
            logging.info("Left Bottom First Four Winner: %s", east_first_four)

        south_first_four = self.right_top.first_four()
        if self.log_results:
            logging.info("Right Top Four Winner: %s", south_first_four)

        midwest_first_four = self.right_bottom.first_four()
        if self.log_results:
            logging.info("Right Bottom First Four Winner: %s", midwest_first_four)

        return west_first_four, east_first_four, south_first_four, midwest_first_four

    def first_round(self):
        west_first_round = self.left_top.first_round()
        if self.log_results:
            logging.info("Left Top First Round Results:")
            logging.info(json.dumps(west_first_round, default=str, indent=2))

        east_first_round = self.left_bottom.first_round()
        if self.log_results:
            logging.info("Left Bottom First Round Results:")
            logging.info(json.dumps(east_first_round, default=str, indent=2))

        south_first_round = self.right_top.first_round()
        if self.log_results:
            logging.info("Right Top First Round Results:")
            logging.info(json.dumps(south_first_round, default=str, indent=2))

        midwest_first_round = self.right_bottom.first_round()
        if self.log_results:
            logging.info("Right Bottom First Round Results:")
            logging.info(json.dumps(midwest_first_round, default=str, indent=2))

        return (
            west_first_round,
            east_first_round,
            south_first_round,
            midwest_first_round,
        )

    def second_round(
        self, west_first_round, east_first_round, south_first_round, midwest_first_round
    ):
        west_second_round = self.left_top.second_round(west_first_round)
        if self.log_results:
            logging.info("Left Top Second Round Results:")
            logging.info(json.dumps(west_second_round, default=str, indent=2))

        east_second_round = self.left_bottom.second_round(east_first_round)
        if self.log_results:
            logging.info("Left Bottom Second Round Results:")
            logging.info(json.dumps(east_second_round, default=str, indent=2))

        south_second_round = self.right_top.second_round(south_first_round)
        if self.log_results:
            logging.info("Right Top Second Round Results:")
            logging.info(json.dumps(south_second_round, default=str, indent=2))

        midwest_second_round = self.right_bottom.second_round(midwest_first_round)
        if self.log_results:
            logging.info("Right Bottom Second Round Results:")
            logging.info(json.dumps(midwest_second_round, default=str, indent=2))

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
        west_sweet_sixteen = self.left_top.sweet_sixteen(west_second_round)
        if self.log_results:
            logging.info("Left Top Sweet Sixteen Results:")
            logging.info(json.dumps(west_sweet_sixteen, default=str, indent=2))

        east_sweet_sixteen = self.left_bottom.sweet_sixteen(east_second_round)
        if self.log_results:
            logging.info("Left Bottom Sweet Sixteen Results:")
            logging.info(json.dumps(east_sweet_sixteen, default=str, indent=2))

        south_sweet_sixteen = self.right_top.sweet_sixteen(south_second_round)
        if self.log_results:
            logging.info("Right Top Sweet Sixteen Results:")
            logging.info(json.dumps(south_sweet_sixteen, default=str, indent=2))

        midwest_sweet_sixteen = self.right_bottom.sweet_sixteen(midwest_second_round)
        if self.log_results:
            logging.info("Right Bottom Sweet Sixteen Results:")
            logging.info(json.dumps(midwest_sweet_sixteen, default=str, indent=2))

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
        west_winner = self.left_top.elite_eight(west_sweet_sixteen)
        if self.log_results:
            logging.info(f"Left Top Group Winner: {west_winner}")

        east_winner = self.left_bottom.elite_eight(east_sweet_sixteen)
        if self.log_results:
            logging.info(f"Left Bottom Group Winner: {east_winner}")

        south_winner = self.right_top.elite_eight(south_sweet_sixteen)
        if self.log_results:
            logging.info(f"Right Top Group Winner: {south_winner}")

        midwest_winner = self.right_bottom.elite_eight(midwest_sweet_sixteen)
        if self.log_results:
            logging.info(f"Right Bottom Group Winner: {midwest_winner}")

        return west_winner, east_winner, south_winner, midwest_winner


class Group:
    def __init__(self, ranking_dict, prediction_method, play_in_rank):
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
        self.play_in_rank = play_in_rank
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
