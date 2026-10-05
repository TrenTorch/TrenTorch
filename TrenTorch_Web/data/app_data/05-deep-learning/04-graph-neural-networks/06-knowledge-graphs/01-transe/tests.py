import numpy as np
from _load import load_solution


_module = load_solution(__file__)
transe_score = _module.transe_score


def test_zero_score():
    h = np.array([1.0, 2.0, 3.0])
    r = np.array([0.5, 0.5, 0.5])
    t = h + r
    score = transe_score(h, r, t)
    assert score < 1e-5


def test_non_zero_score():
    h = np.array([1.0, 0.0, 0.0])
    r = np.array([0.0, 1.0, 0.0])
    t = np.array([0.0, 0.0, 1.0])
    score = transe_score(h, r, t)
    assert score > 0


def test_score_increases_with_error():
    h = np.array([1.0, 2.0, 3.0])
    r = np.array([1.0, 1.0, 1.0])
    t1 = h + r
    t2 = h + r + np.array([1.0, 0.0, 0.0])
    score1 = transe_score(h, r, t1)
    score2 = transe_score(h, r, t2)
    assert score2 > score1


def test_symmetry():
    h = np.array([1.0, 2.0])
    r = np.array([0.5, 0.5])
    t = np.array([2.0, 3.0])
    score = transe_score(h, r, t)
    assert score >= 0


def test_different_dimensions():
    for dim in [1, 5, 10, 50]:
        h = np.random.randn(dim)
        r = np.random.randn(dim)
        t = h + r
        score = transe_score(h, r, t)
        assert score < 1e-5


def test_random_triplets():
    for _ in range(10):
        h = np.random.randn(5)
        r = np.random.randn(5)
        t = np.random.randn(5)
        score = transe_score(h, r, t)
        assert score >= 0 and np.isfinite(score)


def test_scaling():
    h = np.array([1.0, 2.0])
    r = np.array([0.5, 0.5])
    t = np.array([2.0, 3.0])
    score1 = transe_score(h, r, t)
    score2 = transe_score(h * 2, r * 2, t * 2)
    assert np.allclose(score2, score1 * 2)


def test_large_embeddings():
    h = np.random.randn(100)
    r = np.random.randn(100)
    t = h + r + np.random.randn(100) * 0.1
    score = transe_score(h, r, t)
    assert np.isfinite(score) and score >= 0


def test_perfect_relation():
    h = np.ones(5)
    r = np.ones(5) * 2
    t = np.ones(5) * 3
    score = transe_score(h, r, t)
    assert score < 1e-5


def test_negative_values():
    h = np.array([-1.0, -2.0])
    r = np.array([-0.5, -0.5])
    t = h + r
    score = transe_score(h, r, t)
    assert score < 1e-5
