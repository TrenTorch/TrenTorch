"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/05-neural-turing-machines/01-content-weights/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntm-content-weights")
content_weights = _module.content_weights


import numpy as np


def test_1_weights_sum_to_one():
    assert abs(content_weights(np.eye(3), np.array([1.0, 0.0, 0.0]), 2.0).sum() - 1.0) < 1e-12


def test_2_matching_row_gets_most_weight():
    w = content_weights(np.eye(3), np.array([0.0, 1.0, 0.0]), 10.0)
    assert np.argmax(w) == 1


def test_3_zero_sharpness_gives_uniform_weights():
    np.testing.assert_allclose(content_weights(np.eye(4), np.array([1.0, 0.0, 0.0, 0.0]), 0.0), [0.25] * 4, atol=1e-9)


def test_4_output_has_one_weight_per_row():
    assert content_weights(np.ones((5, 2)), np.ones(2), 1.0).shape == (5,)


def test_5_scale_of_key_does_not_change_weights():
    M = np.array([[1.0, 0.0], [0.0, 1.0]])
    a = content_weights(M, np.array([2.0, 1.0]), 3.0)
    b = content_weights(M, np.array([4.0, 2.0]), 3.0)
    np.testing.assert_allclose(a, b, atol=1e-9)


def test_6_does_not_mutate_memory():
    M = np.eye(2)
    content_weights(M, np.ones(2), 1.0)
    np.testing.assert_array_equal(M, np.eye(2))

