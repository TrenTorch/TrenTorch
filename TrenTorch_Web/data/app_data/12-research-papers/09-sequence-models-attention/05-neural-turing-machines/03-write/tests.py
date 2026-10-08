"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/05-neural-turing-machines/03-write/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntm-write")
ntm_write = _module.ntm_write


import numpy as np


def test_1_full_erase_zeroes_the_written_row():
    M = np.array([[1.0, 2.0], [3.0, 4.0]])
    out = ntm_write(M, np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.zeros(2))
    np.testing.assert_allclose(out[0], [0.0, 0.0])


def test_2_add_writes_into_the_row():
    out = ntm_write(np.zeros((2, 2)), np.array([0.0, 1.0]), np.zeros(2), np.array([5.0, 6.0]))
    np.testing.assert_allclose(out[1], [5.0, 6.0])


def test_3_unwritten_rows_are_unchanged():
    M = np.array([[1.0], [2.0]])
    out = ntm_write(M, np.array([0.0, 1.0]), np.array([1.0]), np.array([9.0]))
    np.testing.assert_allclose(out[0], [1.0])


def test_4_keeps_the_shape():
    assert ntm_write(np.ones((3, 2)), np.ones(3) / 3, np.zeros(2), np.ones(2)).shape == (3, 2)


def test_5_zero_write_weights_leave_memory_alone():
    M = np.array([[2.0, 3.0]])
    np.testing.assert_allclose(ntm_write(M, np.zeros(1), np.ones(2), np.ones(2)), M)


def test_6_does_not_mutate_memory():
    M = np.ones((1, 1))
    ntm_write(M, np.ones(1), np.zeros(1), np.ones(1))
    np.testing.assert_array_equal(M, np.ones((1, 1)))

