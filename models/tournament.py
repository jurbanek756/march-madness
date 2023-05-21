#!/usr/bin/env python3

import json
import logging
from models.group import Group


logger = logging.getLogger(__name__)


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
        prediction_method,
        log_results=True,
    ):
        self.log_results = log_results
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
            logger.info("Left Top Group Rankings:")
            logger.info(json.dumps(self.left_top.ranking_dict, default=str, indent=2))
            logger.info("Left Bottom Group Rankings:")
            logger.info(
                json.dumps(self.left_bottom.ranking_dict, default=str, indent=2)
            )
            logger.info("Right Top Group Rankings:")
            logger.info(json.dumps(self.right_top.ranking_dict, default=str, indent=2))
            logger.info("Right Bottom Group Rankings:")
            logger.info(
                json.dumps(self.right_bottom.ranking_dict, default=str, indent=2)
            )
        lt_winner, lb_winner, rt_winner, rb_winner = self.group_winners()
        tournament_winner = self.tournament_winner(
            lt_winner, lb_winner, rt_winner, rb_winner
        )
        if self.log_results:
            logger.info("NCAA Champions: %s", tournament_winner)
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
            logger.info("Championship Game: %s vs. %s", left, right)
        return self.predict(left, right)

    def first_four(self):
        lt = self.left_top.first_four()
        if self.log_results:
            logger.info("Left Top First Four Winner: %s", lt)

        lb = self.left_bottom.first_four()
        if self.log_results:
            logger.info("Left Bottom First Four Winner: %s", lb)

        rt = self.right_top.first_four()
        if self.log_results:
            logger.info("Right Top Four Winner: %s", rt)

        rb = self.right_bottom.first_four()
        if self.log_results:
            logger.info("Right Bottom First Four Winner: %s", rb)

        return lt, lb, rt, rb

    def first_round(self):
        lt = self.left_top.first_round()
        if self.log_results:
            logger.info("Left Top First Round Results:")
            logger.info(json.dumps(lt, default=str, indent=2))

        lb = self.left_bottom.first_round()
        if self.log_results:
            logger.info("Left Bottom First Round Results:")
            logger.info(json.dumps(lb, default=str, indent=2))

        rt = self.right_top.first_round()
        if self.log_results:
            logger.info("Right Top First Round Results:")
            logger.info(json.dumps(rt, default=str, indent=2))

        rb = self.right_bottom.first_round()
        if self.log_results:
            logger.info("Right Bottom First Round Results:")
            logger.info(json.dumps(rb, default=str, indent=2))

        return lt, lb, rt, rb

    def second_round(self, lt_r1, lb_r1, rt_r1, rb_r1):
        lt_result = self.left_top.second_round(lt_r1)
        if self.log_results:
            logger.info("Left Top Second Round Results:")
            logger.info(json.dumps(lt_result, default=str, indent=2))

        lb_result = self.left_bottom.second_round(lb_r1)
        if self.log_results:
            logger.info("Left Bottom Second Round Results:")
            logger.info(json.dumps(lb_result, default=str, indent=2))

        rt_result = self.right_top.second_round(rt_r1)
        if self.log_results:
            logger.info("Right Top Second Round Results:")
            logger.info(json.dumps(rt_result, default=str, indent=2))

        rb_result = self.right_bottom.second_round(rb_r1)
        if self.log_results:
            logger.info("Right Bottom Second Round Results:")
            logger.info(json.dumps(rb_result, default=str, indent=2))

        return lt_result, lb_result, rt_result, rb_result

    def sweet_sixteen(
        self,
        lt,
        lb,
        rt,
        rb,
    ):
        lt_result = self.left_top.sweet_sixteen(lt)
        if self.log_results:
            logger.info("Left Top Sweet Sixteen Results:")
            logger.info(json.dumps(lt_result, default=str, indent=2))

        lb_result = self.left_bottom.sweet_sixteen(lb)
        if self.log_results:
            logger.info("Left Bottom Sweet Sixteen Results:")
            logger.info(json.dumps(lb_result, default=str, indent=2))

        rt_result = self.right_top.sweet_sixteen(rt)
        if self.log_results:
            logger.info("Right Top Sweet Sixteen Results:")
            logger.info(json.dumps(rt_result, default=str, indent=2))

        rb_result = self.right_bottom.sweet_sixteen(rb)
        if self.log_results:
            logger.info("Right Bottom Sweet Sixteen Results:")
            logger.info(json.dumps(rb_result, default=str, indent=2))

        return (
            lt_result,
            lb_result,
            rt_result,
            rb_result,
        )

    def elite_eight(self, lt, lb, rt, rb):
        lt_winner = self.left_top.elite_eight(lt)
        if self.log_results:
            logger.info(f"Left Top Group Winner: {lt_winner}")

        lb_winner = self.left_bottom.elite_eight(lb)
        if self.log_results:
            logger.info(f"Left Bottom Group Winner: {lb_winner}")

        rt_winner = self.right_top.elite_eight(rt)
        if self.log_results:
            logger.info(f"Right Top Group Winner: {rt_winner}")

        rb_winner = self.right_bottom.elite_eight(rb)
        if self.log_results:
            logger.info(f"Right Bottom Group Winner: {rb_winner}")

        return lt_winner, lb_winner, rt_winner, rb_winner