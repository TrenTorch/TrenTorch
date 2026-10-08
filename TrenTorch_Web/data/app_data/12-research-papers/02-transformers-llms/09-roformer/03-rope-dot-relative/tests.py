"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/09-roformer/03-rope-dot-relative/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-rope-relative-dot")
rope_dot = _module.rope_dot


import numpy as np


def test_1_returns_a_float():
    assert isinstance(rope_dot(np.ones(4), np.ones(4), 1, 2), float)


def test_2_depends_only_on_the_offset():
    rng = np.random.default_rng(0)
    q = rng.normal(size=6)
    k = rng.normal(size=6)
    assert abs(rope_dot(q, k, 5, 3) - rope_dot(q, k, 7, 5)) < 1e-9


def test_3_same_position_matches_plain_dot_product():
    rng = np.random.default_rng(1)
    q = rng.normal(size=4)
    k = rng.normal(size=4)
    assert abs(rope_dot(q, k, 9, 9) - float(q @ k)) < 1e-9


def test_4_different_offsets_generally_differ():
    q = np.array([1.0, 0.0, 1.0, 0.0])
    k = np.array([1.0, 0.0, 1.0, 0.0])
    assert abs(rope_dot(q, k, 0, 0) - rope_dot(q, k, 0, 3)) > 1e-6


def test_5_is_symmetric_in_swapping_positions_for_equal_vectors():
    q = np.array([0.5, 1.0])
    assert abs(rope_dot(q, q, 2, 6) - rope_dot(q, q, 6, 2)) < 1e-9


def test_6_does_not_mutate_inputs():
    q = np.array([1.0, 2.0])
    rope_dot(q, np.array([3.0, 4.0]), 1, 2)
    np.testing.assert_array_equal(q, [1.0, 2.0])

