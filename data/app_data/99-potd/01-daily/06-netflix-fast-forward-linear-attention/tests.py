"""
pytest data/app_data/05-transformers-llm/02-modern-transformer-architecture/11-netflix-fast-forward-linear-attention/tests.py
"""

import sys
import tracemalloc
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"99-potd/01-daily/{Path(__file__).resolve().parent.name}"
)
feature_map = _module.feature_map
linear_attention_row_sums = _module.linear_attention_row_sums


def _naive_row_sums(Q, K, V):
    qp, kp = np.maximum(Q, 0.0) + 1.0, np.maximum(K, 0.0) + 1.0
    weights = qp @ kp.T
    out = (weights @ V) / weights.sum(axis=1, keepdims=True)
    return out.sum(axis=1)


def test_feature_map_is_shifted_relu():
    x = np.array([[-2.0, 0.0, 0.5], [3.0, -0.1, 1.0]])
    assert np.allclose(feature_map(x), [[1.0, 1.0, 1.5], [4.0, 1.0, 2.0]])


def test_example_one_matches_the_specs_worked_derivation():
    Q = np.array([[1.0, -2.0], [0.0, 1.0], [-1.0, 0.5]])
    K = np.array([[2.0, -1.0], [0.5, 0.5], [-0.5, 1.0]])
    V = np.array([[1.0, 2.0], [-1.0, 0.5], [0.0, -1.0]])
    result = linear_attention_row_sums(Q, K, V)
    assert np.allclose(result, [0.951613, 0.534483, 0.622449], atol=1e-6)


def test_example_two_all_negative_inputs_average_the_value_rows():
    Q = np.array([[-1.0, -2.0], [-3.0, -1.0]])
    K = np.array([[-1.0, -1.0], [-2.0, -3.0]])
    V = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert np.allclose(linear_attention_row_sums(Q, K, V), [5.0, 5.0], atol=1e-9)


def test_matches_the_quadratic_reference_on_random_inputs():
    rng = np.random.default_rng(0)
    for n, d in [(1, 1), (7, 3), (40, 5), (64, 16)]:
        Q, K, V = (rng.uniform(-10, 10, size=(n, d)) for _ in range(3))
        assert np.allclose(linear_attention_row_sums(Q, K, V), _naive_row_sums(Q, K, V), atol=1e-8)


def test_zeroed_features_never_divide_by_zero():
    rng = np.random.default_rng(1)
    n, d = 50, 4
    Q = -np.abs(rng.normal(size=(n, d))) - 1.0
    K = -np.abs(rng.normal(size=(n, d))) - 1.0
    V = rng.uniform(-5, 5, size=(n, d))
    result = linear_attention_row_sums(Q, K, V)
    assert np.all(np.isfinite(result))
    # phi(Q) = phi(K) = 1 everywhere, so every row averages the value rows.
    assert np.allclose(result, V.mean(axis=0).sum(), atol=1e-9)


def test_d_equals_one_at_the_maximum_sequence_length():
    rng = np.random.default_rng(2)
    n = 100_000
    Q, K, V = (rng.uniform(-10, 10, size=(n, 1)) for _ in range(3))
    result = linear_attention_row_sums(Q, K, V)
    kp = np.maximum(K[:, 0], 0.0) + 1.0
    # With d = 1 the query cancels: every row equals sum(K'V) / sum(K').
    expected = (kp @ V[:, 0]) / kp.sum()
    assert result.shape == (n,)
    assert np.allclose(result, expected, atol=1e-9)


def test_never_materializes_an_n_by_n_matrix():
    rng = np.random.default_rng(3)
    n, d = 6000, 8
    Q, K, V = (rng.uniform(-10, 10, size=(n, d)) for _ in range(3))

    tracemalloc.start()
    try:
        result = linear_attention_row_sums(Q, K, V)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    # A single (6000, 6000) float64 matrix is 288 MB. The linear form needs a
    # few (N, d) temporaries, well under 50 MB.
    assert peak < 50 * 1024 * 1024

    qp, kp = np.maximum(Q, 0.0) + 1.0, np.maximum(K, 0.0) + 1.0
    for i in (0, 1234, n - 1):
        w = kp @ qp[i]
        assert abs(result[i] - ((w @ V) / w.sum()).sum()) < 1e-7


def test_does_not_mutate_its_inputs():
    rng = np.random.default_rng(4)
    Q, K, V = (rng.uniform(-3, 3, size=(20, 4)) for _ in range(3))
    before = (Q.copy(), K.copy(), V.copy())
    linear_attention_row_sums(Q, K, V)
    assert all(np.array_equal(a, b) for a, b in zip((Q, K, V), before))
