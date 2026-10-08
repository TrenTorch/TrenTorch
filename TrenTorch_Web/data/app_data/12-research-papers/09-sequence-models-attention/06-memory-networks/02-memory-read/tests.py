"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/06-memory-networks/02-memory-read/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-memnet-read")
memory_output = _module.memory_output


import numpy as np


def test_1_weighted_sum_of_output_rows():
    np.testing.assert_allclose(memory_output(np.array([0.25, 0.75]), np.array([[4.0], [8.0]])), [7.0])


def test_2_one_hot_selects_a_row():
    np.testing.assert_allclose(memory_output(np.array([0.0, 1.0]), np.array([[1.0, 1.0], [2.0, 3.0]])), [2.0, 3.0])


def test_3_output_has_embedding_dimension():
    assert memory_output(np.ones(4) / 4, np.ones((4, 6))).shape == (6,)


def test_4_uniform_attention_averages():
    np.testing.assert_allclose(memory_output(np.array([0.5, 0.5]), np.array([[0.0], [6.0]])), [3.0])


def test_5_result_is_in_the_convex_hull():
    out = memory_output(np.array([0.2, 0.8]), np.array([[0.0], [10.0]]))
    assert 0.0 <= out[0] <= 10.0


def test_6_does_not_mutate_outputs():
    O = np.ones((2, 2))
    memory_output(np.array([0.5, 0.5]), O)
    np.testing.assert_array_equal(O, np.ones((2, 2)))

