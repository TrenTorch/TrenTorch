"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

step_efficiency = _module.step_efficiency
redundancy_rate = _module.redundancy_rate


def test_1_efficiency_hand_computed():
    assert step_efficiency(10, 4, True) == 0.4


def test_2_failure_scores_zero():
    assert step_efficiency(3, 3, False) == 0.0


def test_3_beating_the_optimum_is_capped():
    assert step_efficiency(2, 5, True) == 1.0


def test_4_redundancy_hand_computed():
    acts = [("search", {"q": "a"}), ("read", {"f": 1}), ("search", {"q": "a"}), ("search", {"q": "b"}), ("read", {"f": 1})]
    assert math.isclose(redundancy_rate(acts), 2 / 5)


def test_5_different_arguments_are_not_repeats():
    assert redundancy_rate([("s", {"q": 1}), ("s", {"q": 2})]) == 0.0


def test_6_argument_key_order_does_not_matter():
    assert redundancy_rate([("s", {"a": 1, "b": 2}), ("s", {"b": 2, "a": 1})]) == 0.5


def test_7_empty_and_inputs_untouched():
    assert redundancy_rate([]) == 0.0
    acts = [("s", {"x": [1]}), ("s", {"x": [1]})]
    snap = [("s", {"x": [1]}), ("s", {"x": [1]})]
    assert redundancy_rate(acts) == 0.5 and acts == snap
