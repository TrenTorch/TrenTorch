"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

success_after_retries = _module.success_after_retries
expected_attempt_cost = _module.expected_attempt_cost
select_plan = _module.select_plan


def test_1_success_probability_hand_computed():
    assert math.isclose(success_after_retries(0.5, 3), 0.875)


def test_2_one_attempt_is_the_base_probability():
    assert math.isclose(success_after_retries(0.3, 1), 0.3)


def test_3_expected_cost_hand_computed():
    # attempts: 1 + 0.5 + 0.25 = 1.75 attempts' worth
    assert math.isclose(expected_attempt_cost(0.5, 10.0, 3), 17.5)


def test_4_certain_success_pays_only_once():
    assert expected_attempt_cost(1.0, 4.0, 5) == 4.0


def test_5_impossible_success_pays_for_every_attempt():
    assert expected_attempt_cost(0.0, 4.0, 5) == 20.0


def test_6_cheap_plan_with_retries_can_beat_an_expensive_reliable_plan():
    plans = [
        {"p": 0.95, "value": 100.0, "cost": 40.0, "attempts": 1},
        {"p": 0.6, "value": 100.0, "cost": 4.0, "attempts": 4},
    ]
    assert select_plan(plans, 1.0) == 1


def test_7_high_cost_weight_flips_the_choice_and_ties_pick_lowest_index():
    plans = [{"p": 0.9, "value": 10.0, "cost": 5.0, "attempts": 1}, {"p": 0.5, "value": 10.0, "cost": 0.1, "attempts": 1}]
    assert select_plan(plans, 0.0) == 0 and select_plan(plans, 10.0) == 1
    assert select_plan([plans[0], dict(plans[0])], 1.0) == 0
