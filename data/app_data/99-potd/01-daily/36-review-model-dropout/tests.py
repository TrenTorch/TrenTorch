"""
pytest data/app_data/99-potd/01-daily/36-review-model-dropout/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
inverted_dropout = _module.inverted_dropout


def test_example_matches_the_specs_worked_values():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    m = np.array([1, 0, 1, 1])
    out = inverted_dropout(x, m, 0.75)
    np.testing.assert_allclose(out, [1.333333, 0.0, 4.0, 5.333333], atol=1e-5)


def test_p_keep_equals_one_is_the_identity():
    x = np.array([1.0, 2.0, 3.0])
    m = np.ones(3)
    np.testing.assert_allclose(inverted_dropout(x, m, 1.0), x, atol=1e-9)


def test_all_zero_mask_gives_all_zero_output():
    x = np.array([5.0, -3.0, 100.0])
    m = np.zeros(3)
    out = inverted_dropout(x, m, 0.5)
    assert not out.any()


def test_very_small_p_keep_stays_finite_and_precise():
    x = np.array([1.0])
    m = np.array([1])
    out = inverted_dropout(x, m, 0.01)
    assert np.isfinite(out[0])
    assert abs(out[0] - 100.0) < 1e-6


def test_matches_a_reference_on_random_masks():
    rng = np.random.default_rng(32)
    for _ in range(20):
        n = rng.integers(1, 1000)
        x = rng.uniform(-10, 10, size=n)
        m = rng.integers(0, 2, size=n)
        p_keep = rng.uniform(0.01, 1.0)
        expected = (x * m) / p_keep
        np.testing.assert_allclose(inverted_dropout(x, m, p_keep), expected, atol=1e-6)
