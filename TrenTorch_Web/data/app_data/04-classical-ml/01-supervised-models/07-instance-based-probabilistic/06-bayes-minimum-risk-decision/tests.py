"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

minimum_risk_class = load_solution(__file__).minimum_risk_class


def test_zero_one_cost_is_argmax_of_posterior():
    cost = 1.0 - np.eye(3)
    rng = np.random.default_rng(0)
    for _ in range(10):
        p = rng.dirichlet(np.ones(3))
        assert minimum_risk_class(p, cost) == int(np.argmax(p))


def test_asymmetric_cost_flips_the_decision():
    # Class 0 is more probable, but wrongly predicting 0 when the truth is
    # class 1 costs 10x more than the reverse.
    p = np.array([0.7, 0.3])
    cost = np.array([[0.0, 1.0], [10.0, 0.0]])
    assert minimum_risk_class(p, cost) == 1


def test_hand_computed_risks():
    p = np.array([0.5, 0.3, 0.2])
    cost = np.array([[0.0, 2.0, 4.0], [1.0, 0.0, 3.0], [5.0, 1.0, 0.0]])
    # risks = [0.3*1 + 0.2*5, 0.5*2 + 0.2*1, 0.5*4 + 0.3*3] = [1.3, 1.2, 2.9]
    assert minimum_risk_class(p, cost) == 1


def test_ties_go_to_smallest_index():
    assert minimum_risk_class(np.array([0.5, 0.5]), np.array([[0.0, 1.0], [1.0, 0.0]])) == 0


def test_certain_posterior_picks_the_free_prediction():
    cost = np.array([[0.0, 5.0], [7.0, 0.0]])
    assert minimum_risk_class(np.array([0.0, 1.0]), cost) == 1


def test_returns_python_int():
    assert isinstance(minimum_risk_class(np.array([0.4, 0.6]), 1.0 - np.eye(2)), int)
