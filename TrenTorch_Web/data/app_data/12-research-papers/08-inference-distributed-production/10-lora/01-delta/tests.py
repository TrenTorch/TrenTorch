"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/10-lora/01-delta/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lora-delta")
lora_delta = _module.lora_delta


import numpy as np


def test_1_hand_value_with_scale_two():
    A = np.array([[1.0, 0.0]])
    B = np.array([[3.0], [4.0]])
    np.testing.assert_allclose(lora_delta(A, B, 2.0, 1), [[6.0, 0.0], [8.0, 0.0]])


def test_2_zero_up_projection_gives_zero_update():
    out = lora_delta(np.ones((2, 3)), np.zeros((4, 2)), 1.0, 2)
    np.testing.assert_allclose(out, 0.0)


def test_3_output_shape_is_out_by_in():
    assert lora_delta(np.ones((2, 5)), np.ones((3, 2)), 1.0, 2).shape == (3, 5)


def test_4_scale_is_alpha_over_rank():
    base = lora_delta(np.ones((1, 2)), np.ones((2, 1)), 1.0, 1)
    scaled = lora_delta(np.ones((1, 2)), np.ones((2, 1)), 4.0, 2)
    np.testing.assert_allclose(scaled, 2 * base)


def test_5_update_has_rank_at_most_r():
    rng = np.random.default_rng(0)
    out = lora_delta(rng.normal(size=(2, 6)), rng.normal(size=(5, 2)), 1.0, 2)
    assert np.linalg.matrix_rank(out) <= 2


def test_6_does_not_mutate_inputs():
    A = np.ones((1, 2))
    lora_delta(A, np.ones((2, 1)), 1.0, 1)
    np.testing.assert_array_equal(A, np.ones((1, 2)))

