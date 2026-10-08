"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/05-neural-turing-machines/02-read/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntm-read")
ntm_read = _module.ntm_read


import numpy as np


def test_1_one_hot_read_returns_one_row():
    np.testing.assert_allclose(ntm_read(np.array([0.0, 1.0]), np.array([[1.0, 2.0], [3.0, 4.0]])), [3.0, 4.0])


def test_2_uniform_read_averages_rows():
    np.testing.assert_allclose(ntm_read(np.array([0.5, 0.5]), np.array([[0.0], [4.0]])), [2.0])


def test_3_output_length_is_memory_width():
    assert ntm_read(np.ones(3) / 3, np.ones((3, 5))).shape == (5,)


def test_4_zero_weights_read_zero():
    np.testing.assert_allclose(ntm_read(np.zeros(2), np.ones((2, 2))), 0.0)


def test_5_hand_value():
    np.testing.assert_allclose(ntm_read(np.array([0.25, 0.75]), np.array([[4.0], [8.0]])), [7.0])


def test_6_does_not_mutate_memory():
    M = np.ones((2, 2))
    ntm_read(np.array([0.5, 0.5]), M)
    np.testing.assert_array_equal(M, np.ones((2, 2)))

