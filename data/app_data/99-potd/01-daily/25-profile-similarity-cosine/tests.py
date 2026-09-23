"""
pytest data/app_data/99-potd/01-daily/25-profile-similarity-cosine/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
cosine_similarity = _module.cosine_similarity

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_value():
    u = np.array([1.0, 2.0, 0.0, 1.0])
    v = np.array([2.0, 0.0, 1.0, 1.0])
    assert abs(cosine_similarity(u, v) - 0.5) < TOLERANCE


def test_either_zero_vector_gives_zero():
    u = np.zeros(3)
    v = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(u, v) == 0.0
    assert cosine_similarity(v, u) == 0.0
    assert cosine_similarity(u, u) == 0.0


def test_identical_vectors_give_exactly_one():
    v = np.array([3.0, -1.0, 4.0, 1.5])
    assert abs(cosine_similarity(v, v) - 1.0) < TOLERANCE


def test_orthogonal_integer_vectors_give_exactly_zero():
    u = np.array([1.0, 0.0])
    v = np.array([0.0, 1.0])
    assert abs(cosine_similarity(u, v)) < TOLERANCE


def test_opposite_vectors_give_exactly_negative_one():
    v = np.array([1.0, 2.0, 3.0])
    assert abs(cosine_similarity(v, -v) - (-1.0)) < TOLERANCE


def test_matches_a_reference_on_random_vectors():
    rng = np.random.default_rng(25)
    for _ in range(20):
        d = rng.integers(1, 1000)
        u = rng.uniform(-10, 10, size=d)
        v = rng.uniform(-10, 10, size=d)
        expected = float(u @ v) / (float(np.linalg.norm(u)) * float(np.linalg.norm(v)))
        assert abs(cosine_similarity(u, v) - expected) < 1e-6
