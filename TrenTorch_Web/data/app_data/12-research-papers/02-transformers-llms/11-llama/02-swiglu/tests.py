"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/11-llama/02-swiglu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-llama-swiglu")
swiglu = _module.swiglu


import numpy as np


def test_1_output_shape_is_sequence_by_hidden():
    assert swiglu(np.ones((3, 4)), np.ones((4, 6)), np.ones((4, 6))).shape == (3, 6)


def test_2_zero_input_gives_zero():
    np.testing.assert_allclose(swiglu(np.zeros((2, 3)), np.ones((3, 2)), np.ones((3, 2))), 0.0)


def test_3_matches_a_hand_computed_case():
    silu_one = 1.0 / (1.0 + np.exp(-1.0))
    out = swiglu(np.array([[1.0]]), np.array([[1.0]]), np.array([[2.0]]))
    np.testing.assert_allclose(out, [[silu_one * 2.0]])


def test_4_zero_gate_projection_gives_zero():
    out = swiglu(np.array([[1.0, 2.0]]), np.zeros((2, 3)), np.ones((2, 3)))
    np.testing.assert_allclose(out, 0.0)


def test_5_large_negative_gate_suppresses_the_output():
    out = swiglu(np.array([[1.0]]), np.array([[-50.0]]), np.array([[3.0]]))
    assert abs(out[0, 0]) < 1e-9


def test_6_does_not_mutate_inputs():
    x = np.ones((1, 2))
    swiglu(x, np.ones((2, 2)), np.ones((2, 2)))
    np.testing.assert_array_equal(x, np.ones((1, 2)))

