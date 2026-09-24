"""
pytest data/app_data/01-numpy/07-linear-algebra/04-vector-norms/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/07-linear-algebra/{Path(__file__).resolve().parent.name}")
l2_norm_from_scratch = _module.l2_norm_from_scratch
l2_norm_builtin = _module.l2_norm_builtin
normalize_vector = _module.normalize_vector


def test_l2_norm_from_scratch_and_builtin_agree():
    for v in [np.array([1.0, 2.0, 3.0]), np.array([-5.0, 12.0]), np.array([0.0, 0.0, 0.0])]:
        np.testing.assert_allclose(l2_norm_from_scratch(v), l2_norm_builtin(v))


def test_known_3_4_5_case():
    v = np.array([3.0, 4.0])
    assert l2_norm_from_scratch(v) == 5.0
    assert l2_norm_builtin(v) == 5.0


def test_normalize_vector_produces_norm_of_1():
    for v in [np.array([3.0, 4.0]), np.array([1.0, 1.0, 1.0]), np.array([10.0, -10.0])]:
        result = normalize_vector(v)
        np.testing.assert_allclose(np.linalg.norm(result), 1.0)


def test_normalize_vector_preserves_direction():
    v = np.array([2.0, 4.0, 6.0])
    result = normalize_vector(v)
    ratios = result / v
    np.testing.assert_allclose(ratios, np.full(3, ratios[0]))
    assert ratios[0] > 0


def test_normalize_vector_does_not_mutate_input():
    v = np.array([3.0, 4.0])
    original = v.copy()
    normalize_vector(v)
    np.testing.assert_array_equal(v, original)
