"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/10-instructgpt/03-clipped-surrogate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ppo-clipped-surrogate")
clipped_surrogate = _module.clipped_surrogate


import numpy as np


def test_1_ratio_one_returns_the_advantage():
    assert abs(float(clipped_surrogate(1.0, 2.0)) - 2.0) < 1e-12


def test_2_large_ratio_with_positive_advantage_is_clipped():
    assert abs(float(clipped_surrogate(1.5, 1.0)) - 1.2) < 1e-12


def test_3_small_ratio_with_positive_advantage_is_not_clipped():
    assert abs(float(clipped_surrogate(0.5, 1.0)) - 0.5) < 1e-12


def test_4_large_ratio_with_negative_advantage_is_not_clipped():
    assert abs(float(clipped_surrogate(1.5, -1.0)) - (-1.5)) < 1e-12


def test_5_works_on_arrays():
    out = clipped_surrogate(np.array([1.0, 1.5]), np.array([1.0, 1.0]), eps=0.2)
    np.testing.assert_allclose(out, [1.0, 1.2])


def test_6_does_not_mutate_inputs():
    r = np.array([1.5])
    clipped_surrogate(r, np.array([1.0]))
    np.testing.assert_array_equal(r, [1.5])

