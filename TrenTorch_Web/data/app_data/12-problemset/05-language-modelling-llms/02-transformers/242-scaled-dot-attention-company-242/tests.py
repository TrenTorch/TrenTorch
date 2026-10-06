"""Tests for causal scaled dot-product attention, with expected values derived from the softmax formula."""
import numpy as np

from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def causal_softmax_rows(scores):
    out = np.zeros_like(scores)
    for i in range(scores.shape[0]):
        row = scores[i, : i + 1]
        e = np.exp(row - row.max())
        out[i, : i + 1] = e / e.sum()
    return out


def reference(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    return causal_softmax_rows(scores) @ V


def test_01_basic_example():
    Q = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(solve(Q, Q, V), reference(Q, Q, V), atol=1e-9)


def test_02_first_position_copies_first_value():
    Q = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(solve(Q, Q, V)[0], [1.0, 2.0], atol=1e-9)


def test_03_zero_queries_average_visible_values():
    Q = np.zeros((2, 2))
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(solve(Q, Q, V), [[1.0, 2.0], [2.0, 3.0]], atol=1e-9)


def test_04_single_token_returns_its_value():
    np.testing.assert_allclose(solve([[2.0, 0.0]], [[1.0, 0.0]], [[5.0, -1.0]]), [[5.0, -1.0]], atol=1e-9)


def test_05_future_values_do_not_leak():
    Q = np.array([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]])
    V = np.array([[0.0, 0.0], [10.0, 0.0], [100.0, 0.0]])
    out = solve(Q, Q, V)
    assert out[0, 0] == 0.0
    assert out[1, 0] < 100.0


def test_06_negative_values():
    Q = np.array([[1.0, -1.0], [-1.0, 1.0]])
    V = np.array([[-1.0, -2.0], [-3.0, -4.0]])
    np.testing.assert_allclose(solve(Q, Q, V), reference(Q, Q, V), atol=1e-9)
