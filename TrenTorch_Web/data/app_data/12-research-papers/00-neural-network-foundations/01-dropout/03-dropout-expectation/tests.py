"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/01-dropout/03-dropout-expectation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dropout-expectation")
dropout_expectation = _module.dropout_expectation


def test_1_output_has_the_same_shape_as_the_input():
    rng = np.random.default_rng(0)
    out = dropout_expectation(np.ones((2, 3)), p=0.5, n_samples=10, rng=rng)
    assert out.shape == (2, 3)


def test_2_zero_drop_probability_returns_the_input_exactly():
    rng = np.random.default_rng(0)
    x = np.array([1.0, -2.0, 3.5])
    np.testing.assert_allclose(dropout_expectation(x, 0.0, 5, rng), x)


def test_3_averages_converge_to_the_input():
    rng = np.random.default_rng(1)
    x = np.array([1.0, 2.0, -3.0])
    out = dropout_expectation(x, p=0.5, n_samples=20000, rng=rng)
    np.testing.assert_allclose(out, x, atol=0.1)


def test_4_single_sample_is_either_zero_or_rescaled():
    rng = np.random.default_rng(2)
    out = dropout_expectation(np.array([4.0]), p=0.5, n_samples=1, rng=rng)
    assert out[0] in (0.0, 8.0)


def test_5_same_seed_gives_same_result():
    a = dropout_expectation(np.ones(4), 0.3, 50, np.random.default_rng(7))
    b = dropout_expectation(np.ones(4), 0.3, 50, np.random.default_rng(7))
    np.testing.assert_array_equal(a, b)


def test_6_does_not_mutate_the_input():
    x = np.array([1.0, 2.0])
    dropout_expectation(x, 0.5, 10, np.random.default_rng(3))
    np.testing.assert_array_equal(x, [1.0, 2.0])

