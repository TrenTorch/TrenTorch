"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/10-vq-vae/01-nearest-code/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vq-nearest-code")
nearest_code_index = _module.nearest_code_index


import numpy as np


def test_1_exact_match_returns_its_index():
    codebook = np.array([[0.0, 0.0], [1.0, 1.0], [5.0, 5.0]])
    assert nearest_code_index(np.array([1.0, 1.0]), codebook) == 1


def test_2_picks_the_closer_of_two_codes():
    codebook = np.array([[0.0], [10.0]])
    assert nearest_code_index(np.array([3.0]), codebook) == 0


def test_3_returns_a_python_int():
    assert isinstance(nearest_code_index(np.array([0.0]), np.array([[0.0], [1.0]])), int)


def test_4_ties_pick_the_first_code():
    codebook = np.array([[-1.0], [1.0]])
    assert nearest_code_index(np.array([0.0]), codebook) == 0


def test_5_works_in_higher_dimensions():
    codebook = np.eye(4)
    assert nearest_code_index(np.array([0.0, 0.0, 0.9, 0.0]), codebook) == 2


def test_6_does_not_mutate_inputs():
    z = np.array([2.0])
    nearest_code_index(z, np.array([[0.0], [4.0]]))
    np.testing.assert_array_equal(z, [2.0])

