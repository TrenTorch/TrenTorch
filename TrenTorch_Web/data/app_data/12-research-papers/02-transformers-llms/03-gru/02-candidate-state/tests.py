"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/03-gru/02-candidate-state/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gru-candidate")
gru_candidate = _module.gru_candidate


import numpy as np


def test_1_zero_inputs_give_zero():
    out = gru_candidate(np.zeros(2), np.zeros(3), np.ones(3), np.ones((3, 2)), np.ones((3, 3)))
    np.testing.assert_allclose(out, 0.0)


def test_2_reset_gate_zero_ignores_previous_state():
    x = np.array([1.0])
    a = gru_candidate(x, np.array([5.0]), np.array([0.0]), np.array([[1.0]]), np.array([[7.0]]))
    b = gru_candidate(x, np.array([-3.0]), np.array([0.0]), np.array([[1.0]]), np.array([[7.0]]))
    np.testing.assert_allclose(a, b)
    np.testing.assert_allclose(a, [np.tanh(1.0)])


def test_3_reset_gate_one_uses_previous_state():
    out = gru_candidate(np.array([0.0]), np.array([1.0]), np.array([1.0]), np.array([[0.0]]), np.array([[1.0]]))
    np.testing.assert_allclose(out, [np.tanh(1.0)])


def test_4_output_is_bounded_by_one():
    out = gru_candidate(np.array([50.0]), np.array([50.0]), np.array([1.0]), np.array([[1.0]]), np.array([[1.0]]))
    assert np.all(np.abs(out) <= 1.0)


def test_5_output_shape_is_hidden_size():
    assert gru_candidate(np.ones(2), np.ones(4), np.ones(4), np.ones((4, 2)), np.ones((4, 4))).shape == (4,)


def test_6_does_not_mutate_inputs():
    h = np.array([0.5])
    gru_candidate(np.array([1.0]), h, np.array([1.0]), np.array([[1.0]]), np.array([[1.0]]))
    np.testing.assert_array_equal(h, [0.5])

