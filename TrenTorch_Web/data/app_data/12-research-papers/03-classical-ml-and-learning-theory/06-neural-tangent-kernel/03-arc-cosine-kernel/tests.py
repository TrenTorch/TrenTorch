"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/06-neural-tangent-kernel/03-arc-cosine-kernel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ntk-arc-cosine")
arc_cosine_kernel = _module.arc_cosine_kernel


import math

import numpy as np


def test_1_self_kernel_is_half_the_squared_norm():
    x = np.array([3.0, 4.0])
    assert abs(arc_cosine_kernel(x, x) - 12.5) < 1e-6


def test_2_orthogonal_inputs_match_the_formula():
    x = np.array([1.0, 0.0])
    y = np.array([0.0, 2.0])
    assert abs(arc_cosine_kernel(x, y) - (1 * 2) / (2 * math.pi)) < 1e-9


def test_3_is_symmetric():
    x = np.array([1.0, 2.0])
    y = np.array([-1.0, 0.5])
    assert abs(arc_cosine_kernel(x, y) - arc_cosine_kernel(y, x)) < 1e-12


def test_4_is_nonnegative():
    rng = np.random.default_rng(0)
    for _ in range(20):
        assert arc_cosine_kernel(rng.normal(size=3), rng.normal(size=3)) >= -1e-12


def test_5_zero_vector_gives_zero():
    assert arc_cosine_kernel(np.zeros(2), np.array([1.0, 1.0])) == 0.0


def test_6_returns_a_float():
    assert isinstance(arc_cosine_kernel(np.array([1.0]), np.array([1.0])), float)

