"""
pytest data/01-classical-ml/02-classification/01-sigmoid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

sigmoid = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").sigmoid


def test_zero_input_gives_half():
    assert np.isclose(sigmoid(np.array([0.0])), 0.5)


def test_output_always_in_open_interval():
    # Bounded to +-25, not further: float64 itself saturates sigmoid to
    # exactly 0.0/1.0 well before z=50 (1 + exp(-40) already rounds to
    # exactly 1.0 in double precision) -- that's expected float64
    # behavior, not a bug, and is exactly what the extreme-values test
    # below accepts as correct. This test checks the *mathematical*
    # open-interval property in a range where floating point doesn't
    # already erase it.
    z = np.linspace(-25, 25, 200)
    p = sigmoid(z)
    assert np.all(p > 0.0) and np.all(p < 1.0)


def test_monotonically_increasing():
    z = np.sort(np.random.default_rng(0).normal(size=100))
    p = sigmoid(z)
    assert np.all(np.diff(p) >= 0)


def test_extreme_values_do_not_overflow_or_nan():
    # The actual reason this function exists instead of a naive
    # 1/(1+exp(-z)) one-liner: exp(50000) overflows without warning
    # handling, silently producing nan through the division.
    z = np.array([-1e5, 1e5, -500, 500])
    p = sigmoid(z)
    assert np.all(np.isfinite(p))
    assert np.allclose(p, [0.0, 1.0, 0.0, 1.0], atol=1e-6)


def test_symmetric_around_zero():
    # sigmoid(-z) == 1 - sigmoid(z) is a real mathematical identity, not
    # a coincidence -- a broken implementation (e.g. wrong sign in the
    # exponent) usually violates this even while passing single-point tests.
    z = np.array([0.3, 1.7, -2.2, 5.0])
    assert np.allclose(sigmoid(-z), 1 - sigmoid(z))


def test_batch_shape_preserved():
    z = np.random.default_rng(1).normal(size=(10, 5))
    assert sigmoid(z).shape == (10, 5)
