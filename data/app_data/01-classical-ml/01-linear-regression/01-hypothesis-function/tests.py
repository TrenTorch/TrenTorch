"""
pytest data/app_data/01-classical-ml/01-linear-regression/01-hypothesis-function/tests.py

Tests are numbered on purpose. The app's "Run" button shows only the
first couple of tests (sorted by name) as a quick sanity check; "Submit"
runs every test below. Numbering keeps both views in the same
deliberate order: simple hand-computed cases first, then shape/bias
coverage, then edge cases, then tests aimed at catching specific,
plausible wrong implementations (a transpose forgotten, a bias
broadcast on the wrong axis), and finally the large-scale correctness
oracle.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).linear


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_feature_single_output_matches_hand_computation():
    # Simplest possible case: one in-feature, one out-feature, one sample.
    # y = 2*3 + 1 = 7 -- catches basic wiring bugs before anything else.
    input = np.array([[3.0]])
    weight = np.array([[2.0]])
    bias = np.array([1.0])
    assert np.allclose(linear(input, weight, bias), [[7.0]])


def test_02_multi_feature_matches_hand_computation():
    # Two in-features, two samples -- makes sure weight gets transposed the
    # right way (a common bug: input @ weight instead of input @ weight.T,
    # which only "accidentally" works when weight happens to be square).
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0]])  # out_features=1, in_features=2
    assert np.allclose(linear(input, weight, None), [[3.0], [7.0]])


# --- Shape / general in-features vs. out-features cases --------------------


def test_03_multiple_output_features():
    # out_features > 1 -- the general case every real nn.Linear handles,
    # not just single-output regression. Each output column is an
    # independent linear combination of the same input row.
    input = np.array([[1.0, 0.0], [0.0, 1.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # out_features=3
    result = linear(input, weight, None)
    expected = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    assert np.allclose(result, expected)


def test_04_output_is_never_squeezed():
    # Real torch.nn.functional.linear never collapses out_features=1 down
    # to a 1-D output -- (batch_size, 1) it is, every time. Squeezing here
    # is exactly the bug Theory warns about: it looks harmless and then
    # silently broadcasts wrong against a (batch_size,) target two
    # questions from now.
    input = np.random.randn(10, 4)
    weight = np.random.randn(1, 4)
    result = linear(input, weight, np.array([0.5]))
    assert result.shape == (10, 1)


# --- Bias handling -----------------------------------------------------


def test_05_bias_none_means_no_bias_term():
    # bias=None is a real, supported call, not an error case. With it, the
    # output is exactly input @ weight.T -- nothing added.
    input = np.random.randn(5, 3)
    weight = np.random.randn(2, 3)
    result = linear(input, weight, None)
    assert np.allclose(result, input @ weight.T)


def test_06_zero_weight_returns_bias_for_every_row():
    # Isolates the bias term from the weight term: with weight all zero,
    # every output row must collapse to exactly bias, regardless of input.
    input = np.random.randn(5, 3)
    weight = np.zeros((2, 3))
    bias = np.array([1.5, -2.5])
    result = linear(input, weight, bias)
    assert np.allclose(result, np.tile(bias, (5, 1)))


def test_07_bias_adds_along_out_features_not_batch():
    # A specific, plausible bug: broadcasting bias against the wrong axis
    # (e.g. adding it per-sample instead of per-output-feature). Uses a
    # different bias value per output feature and more than one sample,
    # so a wrong-axis broadcast either crashes (shape mismatch) or gives
    # every row the same *wrong* pattern instead of the same right one.
    input = np.zeros((4, 2))  # weight term contributes nothing
    weight = np.zeros((3, 2))
    bias = np.array([10.0, 20.0, 30.0])
    result = linear(input, weight, bias)
    for row in result:
        assert np.array_equal(row, bias)


# --- Edge cases ----------------------------------------------------------


def test_08_single_sample_batch():
    # batch_size=1 is an easy edge case to break with careless indexing
    # or an implicit assumption that there's more than one row.
    input = np.array([[1.0, 2.0, 3.0]])
    weight = np.array([[1.0, 0.0, -1.0], [0.5, 0.5, 0.5]])
    result = linear(input, weight, None)
    assert result.shape == (1, 2)
    assert np.allclose(result, [[-2.0, 3.0]])


def test_09_single_in_feature():
    # in_features=1 -- weight collapses to a column, easy to transpose
    # incorrectly and not notice because the shapes still "work".
    input = np.array([[2.0], [3.0], [4.0]])
    weight = np.array([[5.0]])
    result = linear(input, weight, np.array([1.0]))
    assert np.allclose(result, [[11.0], [16.0], [21.0]])


def test_10_dtype_is_preserved():
    # No dtype cast happens anywhere on purpose -- whatever dtype `input`
    # arrives in should pass straight through.
    input = np.array([[1.0, 2.0]], dtype=np.float32)
    weight = np.array([[1.0, 1.0]], dtype=np.float32)
    result = linear(input, weight, None)
    assert result.dtype == np.float32


# --- Mutation-catching regression cases -------------------------------


def test_11_transposed_weight_is_actually_required():
    # Directly targets the "forgot weight.T" mutant: with a rectangular,
    # non-symmetric weight, input @ weight (no transpose) either crashes
    # on a shape mismatch or -- if it happens to be shape-compatible --
    # produces a numerically different result from the correct
    # input @ weight.T. Either way, this fails for that specific bug.
    input = np.array([[1.0, 2.0, 3.0]])
    weight = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])  # (2, 3)
    result = linear(input, weight, None)
    assert np.allclose(result, [[1.0, 2.0]])


def test_12_does_not_mutate_its_inputs():
    # A vectorized expression should never need to write back into
    # input/weight/bias -- if it does, it's either not truly vectorized
    # or doing something more surprising than "compute and return".
    input = np.array([[1.0, 2.0]])
    weight = np.array([[1.0, 1.0]])
    bias = np.array([1.0])
    input_copy, weight_copy, bias_copy = input.copy(), weight.copy(), bias.copy()
    linear(input, weight, bias)
    assert np.array_equal(input, input_copy)
    assert np.array_equal(weight, weight_copy)
    assert np.array_equal(bias, bias_copy)


# --- Full correctness oracle -----------------------------------------


def test_13_large_random_batch_matches_manual_loop():
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
