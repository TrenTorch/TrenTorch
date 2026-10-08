"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/12-switch-transformer/02-load-balancing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-switch-load-balancing")
load_balancing_loss = _module.load_balancing_loss


import numpy as np


def test_1_perfectly_balanced_routing_gives_one():
    E = 4
    idx = np.arange(8) % E
    probs = np.full((8, E), 1.0 / E)
    assert abs(load_balancing_loss(idx, probs, E) - 1.0) < 1e-12


def test_2_everything_on_one_expert_with_full_confidence_gives_e():
    E = 4
    idx = np.zeros(5, dtype=int)
    probs = np.zeros((5, E))
    probs[:, 0] = 1.0
    assert abs(load_balancing_loss(idx, probs, E) - E) < 1e-12


def test_3_collapsed_routing_is_worse_than_balanced():
    E = 3
    balanced = load_balancing_loss(np.array([0, 1, 2]), np.full((3, E), 1 / 3), E)
    collapsed_probs = np.zeros((3, E))
    collapsed_probs[:, 0] = 1.0
    collapsed = load_balancing_loss(np.array([0, 0, 0]), collapsed_probs, E)
    assert collapsed > balanced


def test_4_returns_a_python_float():
    assert isinstance(load_balancing_loss(np.array([0]), np.array([[1.0, 0.0]]), 2), float)


def test_5_matches_a_hand_computed_case():
    # f = [0.5, 0.5], P = [0.8, 0.2] -> 2 * (0.4 + 0.1) = 1.0
    idx = np.array([0, 1])
    probs = np.array([[0.8, 0.2], [0.8, 0.2]])
    assert abs(load_balancing_loss(idx, probs, 2) - 1.0) < 1e-12


def test_6_does_not_mutate_inputs():
    probs = np.full((2, 2), 0.5)
    load_balancing_loss(np.array([0, 1]), probs, 2)
    np.testing.assert_array_equal(probs, np.full((2, 2), 0.5))

