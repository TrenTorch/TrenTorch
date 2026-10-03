"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

cost_per_success = _module.cost_per_success
pareto_front = _module.pareto_front


def test_1_cost_per_success_hand_computed():
    assert math.isclose(cost_per_success([1.0, 2.0, 3.0, 4.0], [True, False, True, False]), 5.0)


def test_2_no_successes_is_infinite():
    assert cost_per_success([1.0, 1.0], [False, False]) == float("inf")


def test_3_failures_still_count_toward_cost():
    assert cost_per_success([1.0, 9.0], [True, False]) == 10.0


def test_4_pareto_front_hand_computed():
    pts = [(1.0, 0.5), (2.0, 0.7), (3.0, 0.6), (4.0, 0.9)]
    # (3.0, 0.6) is dominated by (2.0, 0.7)
    assert pareto_front(pts) == [0, 1, 3]


def test_5_identical_points_do_not_dominate_each_other():
    assert pareto_front([(1.0, 0.5), (1.0, 0.5)]) == [0, 1]


def test_6_cheaper_and_better_dominates():
    assert pareto_front([(5.0, 0.4), (2.0, 0.8)]) == [1]


def test_7_equal_cost_higher_rate_dominates_and_input_untouched():
    pts = [(2.0, 0.5), (2.0, 0.7)]
    snap = list(pts)
    assert pareto_front(pts) == [1] and pts == snap
