"""
pytest data/app_data/01-classical-ml/01-linear-regression/01-hypothesis-function/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).linear


def test_single_feature_single_output_matches_hand_computation():
    # Simplest possible case: one in-feature, one out-feature, one sample.
    # y = 2*3 + 1 = 7 -- catches basic wiring bugs before anything else.
    input = np.array([[3.0]])
    weight = np.array([[2.0]])
    bias = np.array([1.0])
    assert np.allclose(linear(input, weight, bias), [[7.0]])


def test_multi_feature_matches_hand_computation():
    # Two in-features, two samples -- makes sure weight gets transposed the
    # right way (a common bug: input @ weight instead of input @ weight.T,
    # which only "accidentally" works when weight happens to be square).
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0]])  # out_features=1, in_features=2
    assert np.allclose(linear(input, weight, None), [[3.0], [7.0]])


def test_output_is_never_squeezed():
    # Real torch.nn.functional.linear never collapses out_features=1 down
    # to a 1-D output -- (batch_size, 1) it is, every time. Squeezing here
    # is exactly the bug Theory warns about: it looks harmless and then
    # silently broadcasts wrong against a (batch_size,) target two
    # questions from now.
    input = np.random.randn(10, 4)
    weight = np.random.randn(1, 4)
    result = linear(input, weight, np.array([0.5]))
    assert result.shape == (10, 1)


def test_multiple_output_features():
    # out_features > 1 -- the general case every real nn.Linear handles,
    # not just single-output regression. Each output column is an
    # independent linear combination of the same input row.
    input = np.array([[1.0, 0.0], [0.0, 1.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # out_features=3
    result = linear(input, weight, None)
    expected = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    assert np.allclose(result, expected)


def test_bias_none_means_no_bias_term():
    # bias=None is a real, supported call, not an error case. With it, the
    # output is exactly input @ weight.T -- nothing added.
    input = np.random.randn(5, 3)
    weight = np.random.randn(2, 3)
    result = linear(input, weight, None)
    assert np.allclose(result, input @ weight.T)


def test_zero_weight_returns_bias_for_every_row():
    # Isolates the bias term from the weight term: with weight all zero,
    # every output row must collapse to exactly bias, regardless of input.
    input = np.random.randn(5, 3)
    weight = np.zeros((2, 3))
    bias = np.array([1.5, -2.5])
    result = linear(input, weight, bias)
    assert np.allclose(result, np.tile(bias, (5, 1)))


def test_dtype_is_preserved():
    # No dtype cast happens anywhere on purpose -- whatever dtype `input`
    # arrives in should pass straight through.
    input = np.array([[1.0, 2.0]], dtype=np.float32)
    weight = np.array([[1.0, 1.0]], dtype=np.float32)
    result = linear(input, weight, None)
    assert result.dtype == np.float32


def test_large_random_batch_matches_manual_loop():
    # The real correctness bar: compare the vectorized implementation
    # against a naive per-sample, per-output-feature Python loop on a
    # large random batch. If they ever disagree, the vectorized version
    # has a bug -- the loop version is slow but effectively impossible to
    # get subtly wrong.
    rng = np.random.default_rng(0)
    input = rng.normal(size=(200, 20))
    weight = rng.normal(size=(5, 20))
    bias = rng.normal(size=5)
    vectorized = linear(input, weight, bias)
    manual = np.array(
        [[input[i] @ weight[j] + bias[j] for j in range(5)] for i in range(200)]
    )
    assert np.allclose(vectorized, manual)
