"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/05-adversarial-autoencoders/01-reconstruction-mse/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-aae-recon-mse")
reconstruction_mse = _module.reconstruction_mse


import numpy as np


def test_1_perfect_reconstruction_gives_zero():
    x = np.array([[1.0, 2.0]])
    assert reconstruction_mse(x, x) == 0.0


def test_2_hand_value():
    assert abs(reconstruction_mse(np.array([0.0, 0.0]), np.array([1.0, 3.0])) - 5.0) < 1e-12


def test_3_symmetric_in_its_arguments():
    a = np.array([1.0, 4.0])
    b = np.array([2.0, 2.0])
    assert reconstruction_mse(a, b) == reconstruction_mse(b, a)


def test_4_returns_a_python_float():
    assert isinstance(reconstruction_mse(np.ones(2), np.zeros(2)), float)


def test_5_error_scales_quadratically():
    a = reconstruction_mse(np.zeros(1), np.array([1.0]))
    b = reconstruction_mse(np.zeros(1), np.array([2.0]))
    assert abs(b - 4 * a) < 1e-12


def test_6_does_not_mutate_inputs():
    x = np.array([1.0])
    reconstruction_mse(x, np.zeros(1))
    np.testing.assert_array_equal(x, [1.0])

