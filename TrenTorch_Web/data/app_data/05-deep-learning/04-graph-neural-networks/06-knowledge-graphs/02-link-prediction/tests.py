import numpy as np
from _load import load_solution


_module = load_solution(__file__)
link_prediction_score = _module.link_prediction_score


def test_dot_product():
    u = np.array([1.0, 0.0, 0.0])
    v = np.array([1.0, 0.0, 0.0])
    score = link_prediction_score(u, v, method='dot')
    assert np.isclose(score, 1.0)


def test_dot_orthogonal():
    u = np.array([1.0, 0.0])
    v = np.array([0.0, 1.0])
    score = link_prediction_score(u, v, method='dot')
    assert np.isclose(score, 0.0)


def test_euclidean_identical():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([1.0, 2.0, 3.0])
    score = link_prediction_score(u, v, method='euclidean')
    assert np.isclose(score, 0.0)


def test_euclidean_negative():
    u = np.array([0.0, 0.0])
    v = np.array([1.0, 0.0])
    score = link_prediction_score(u, v, method='euclidean')
    assert score < 0


def test_cosine_identical():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([1.0, 2.0, 3.0])
    score = link_prediction_score(u, v, method='cosine')
    assert np.isclose(score, 1.0)


def test_cosine_opposite():
    u = np.array([1.0, 0.0])
    v = np.array([-1.0, 0.0])
    score = link_prediction_score(u, v, method='cosine')
    assert np.isclose(score, -1.0)


def test_different_methods():
    u = np.array([1.0, 2.0])
    v = np.array([2.0, 1.0])
    dot = link_prediction_score(u, v, method='dot')
    euc = link_prediction_score(u, v, method='euclidean')
    cos = link_prediction_score(u, v, method='cosine')
    assert not np.isclose(dot, euc)


def test_large_embeddings():
    u = np.random.randn(100)
    v = np.random.randn(100)
    for method in ['dot', 'euclidean', 'cosine']:
        score = link_prediction_score(u, v, method=method)
        assert np.isfinite(score)


def test_zero_embeddings():
    u = np.zeros(5)
    v = np.random.randn(5)
    for method in ['dot', 'euclidean', 'cosine']:
        score = link_prediction_score(u, v, method=method)
        assert np.isfinite(score)


def test_invalid_method():
    u = np.array([1.0, 2.0])
    v = np.array([3.0, 4.0])
    try:
        link_prediction_score(u, v, method='invalid')
        assert False
    except ValueError:
        pass
