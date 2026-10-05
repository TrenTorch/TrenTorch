"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/03-gru/01-update-gate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gru-update-gate")
gru_update_gate = _module.gru_update_gate


import numpy as np


def test_1_zero_inputs_give_one_half():
    np.testing.assert_allclose(gru_update_gate(np.zeros(2), np.zeros(3), np.ones((3, 2)), np.ones((3, 3))), 0.5)


def test_2_output_shape_is_hidden_size():
    assert gru_update_gate(np.ones(4), np.ones(5), np.ones((5, 4)), np.ones((5, 5))).shape == (5,)


def test_3_values_are_in_open_unit_interval():
    rng = np.random.default_rng(0)
    z = gru_update_gate(rng.normal(size=3) * 4, rng.normal(size=2) * 4, rng.normal(size=(2, 3)), rng.normal(size=(2, 2)))
    assert np.all(z > 0) and np.all(z < 1)


def test_4_large_positive_pre_activation_saturates_near_one():
    z = gru_update_gate(np.array([1.0]), np.array([0.0]), np.array([[50.0]]), np.array([[0.0]]))
    assert abs(z[0] - 1.0) < 1e-6


def test_5_matches_a_hand_computed_case():
    z = gru_update_gate(np.array([1.0]), np.array([0.0]), np.array([[0.0]]), np.array([[0.0]]))
    np.testing.assert_allclose(z, [0.5])


def test_6_does_not_mutate_inputs():
    h = np.array([0.1])
    gru_update_gate(np.array([1.0]), h, np.array([[1.0]]), np.array([[1.0]]))
    np.testing.assert_array_equal(h, [0.1])

