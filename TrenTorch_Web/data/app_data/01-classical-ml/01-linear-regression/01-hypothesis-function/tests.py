"""
pytest data/app_data/01-classical-ml/01-linear-regression/01-hypothesis-function/tests.py

Tests are numbered on purpose. The app's "Run" button shows only the
first couple of tests (sorted by name) as a quick sanity check; "Submit"
runs every test below. Numbering keeps both views in the same
deliberate order: simple hand-computed cases first, then shape/bias
coverage, edge cases, array-hygiene checks (non-contiguous memory,
read-only inputs), tests aimed at specific plausible wrong
implementations (a dropped transpose, a wrong-axis bias broadcast), and
finally two independent correctness oracles -- one against a naive
per-sample loop, one against real torch.nn.functional.linear.
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


def test_05_square_shape_is_not_a_special_case():
    # out_features == in_features can accidentally hide a "forgot to
    # transpose" bug, since input @ weight and input @ weight.T are both
    # shape-valid here. Uses an asymmetric weight (weight != weight.T) so
    # the two give numerically different, distinguishable results.
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 0.0], [5.0, 1.0]])  # not symmetric
    result = linear(input, weight, None)
    # Row 0: [1*1+0*2, 5*1+1*2] = [1, 7]; Row 1: [1*3+0*4, 5*3+1*4] = [3, 19]
    assert np.allclose(result, [[1.0, 7.0], [3.0, 19.0]])


# --- Bias handling -----------------------------------------------------


def test_06_bias_none_means_no_bias_term():
    # bias=None is a real, supported call, not an error case. With it, the
    # output is exactly input @ weight.T -- nothing added.
    input = np.random.randn(5, 3)
    weight = np.random.randn(2, 3)
    result = linear(input, weight, None)
    assert np.allclose(result, input @ weight.T)


def test_07_zero_weight_returns_bias_for_every_row():
    # Isolates the bias term from the weight term: with weight all zero,
    # every output row must collapse to exactly bias, regardless of input.
    input = np.random.randn(5, 3)
    weight = np.zeros((2, 3))
    bias = np.array([1.5, -2.5])
    result = linear(input, weight, bias)
    assert np.allclose(result, np.tile(bias, (5, 1)))


def test_08_bias_adds_along_out_features_not_batch():
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


def test_09_negative_and_fractional_values():
    # Nothing in the operation should care about sign or magnitude --
    # a solution that quietly assumes non-negative inputs (e.g. via some
    # accidental abs() or clip()) fails here.
    input = np.array([[-1.5, 2.25], [0.0, -3.75]])
    weight = np.array([[-2.0, 0.5], [1.0, -1.0]])
    bias = np.array([-0.5, 2.0])
    result = linear(input, weight, bias)
    expected = np.array(
        [
            [-1.5 * -2.0 + 2.25 * 0.5 - 0.5, -1.5 * 1.0 + 2.25 * -1.0 + 2.0],
            [0.0 * -2.0 + -3.75 * 0.5 - 0.5, 0.0 * 1.0 + -3.75 * -1.0 + 2.0],
        ]
    )
    assert np.allclose(result, expected)


# --- Edge cases ----------------------------------------------------------


def test_10_single_sample_batch():
    # batch_size=1 is an easy edge case to break with careless indexing
    # or an implicit assumption that there's more than one row.
    input = np.array([[1.0, 2.0, 3.0]])
    weight = np.array([[1.0, 0.0, -1.0], [0.5, 0.5, 0.5]])
    result = linear(input, weight, None)
    assert result.shape == (1, 2)
    assert np.allclose(result, [[-2.0, 3.0]])


def test_11_single_in_feature():
    # in_features=1 -- weight collapses to a column, easy to transpose
    # incorrectly and not notice because the shapes still "work".
    input = np.array([[2.0], [3.0], [4.0]])
    weight = np.array([[5.0]])
    result = linear(input, weight, np.array([1.0]))
    assert np.allclose(result, [[11.0], [16.0], [21.0]])


def test_12_many_output_features_single_sample():
    # Stress the out_features axis specifically, independent of batch
    # size: one sample, a large number of output features, each of which
    # must come out as an independent linear combination.
    rng = np.random.default_rng(21)
    input = rng.normal(size=(1, 5))
    weight = rng.normal(size=(64, 5))
    bias = rng.normal(size=64)
    result = linear(input, weight, bias)
    assert result.shape == (1, 64)
    assert np.allclose(result[0], weight @ input[0] + bias)


def test_13_dtype_is_preserved():
    # No dtype cast happens anywhere on purpose -- whatever dtype `input`
    # arrives in should pass straight through.
    input = np.array([[1.0, 2.0]], dtype=np.float32)
    weight = np.array([[1.0, 1.0]], dtype=np.float32)
    result = linear(input, weight, None)
    assert result.dtype == np.float32


# --- Array hygiene: memory layout and mutability ---------------------


def test_14_works_on_non_contiguous_arrays():
    # A slice like arr[:, ::2] is a real, valid NumPy array but is NOT
    # C-contiguous in memory. An implementation that assumes contiguity
    # (e.g. via a raw .reshape() that only works on contiguous data) can
    # crash or silently misbehave here even though `input @ weight.T`
    # itself handles non-contiguous arrays completely correctly.
    base = np.arange(24.0).reshape(4, 6)
    input = base[:, ::2]  # shape (4, 3), non-contiguous
    assert not input.flags["C_CONTIGUOUS"]
    weight = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 1.0]])
    result = linear(input, weight, None)
    assert np.allclose(result, input.copy() @ weight.T)


def test_15_does_not_require_writable_inputs():
    # Real training code frequently hands this function a read-only view
    # (e.g. a slice of a larger batch array marked read-only on purpose,
    # to catch accidental in-place edits elsewhere in a pipeline). A
    # correct, purely-computing implementation never needs to write into
    # input/weight/bias, so it must work unchanged when they're read-only.
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0]])
    bias = np.array([0.5])
    for arr in (input, weight, bias):
        arr.setflags(write=False)
    result = linear(input, weight, bias)
    assert np.allclose(result, [[3.5], [7.5]])


def test_16_does_not_mutate_its_inputs():
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


# --- Mutation-catching regression case ---------------------------------


def test_17_transposed_weight_is_actually_required():
    # Directly targets the "forgot weight.T" mutant: with a rectangular,
    # non-symmetric weight, input @ weight (no transpose) either crashes
    # on a shape mismatch or -- if it happens to be shape-compatible --
    # produces a numerically different result from the correct
    # input @ weight.T. Either way, this fails for that specific bug.
    input = np.array([[1.0, 2.0, 3.0]])
    weight = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])  # (2, 3)
    result = linear(input, weight, None)
    assert np.allclose(result, [[1.0, 2.0]])


# --- Independent correctness oracles ----------------------------------


def test_18_matches_manual_loop_across_several_random_shapes():
    # Compares the vectorized implementation against a naive per-sample,
    # per-output-feature Python loop -- across several unrelated random
    # shapes and seeds, not just one. If they ever disagree on any of
    # these, the vectorized version has a bug; the loop version is slow
    # but effectively impossible to get subtly wrong.
    configs = [
        (0, 200, 20, 5),
        (1, 1, 8, 3),
        (2, 50, 1, 1),
        (3, 17, 6, 9),
    ]
    for seed, batch_size, in_features, out_features in configs:
        rng = np.random.default_rng(seed)
        input = rng.normal(size=(batch_size, in_features))
        weight = rng.normal(size=(out_features, in_features))
        bias = rng.normal(size=out_features)
        vectorized = linear(input, weight, bias)
        manual = np.array(
            [
                [input[i] @ weight[j] + bias[j] for j in range(out_features)]
                for i in range(batch_size)
            ]
        )
        assert np.allclose(vectorized, manual), f"mismatch for shape config seed={seed}"


def test_19_matches_real_pytorch_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(0)
    #   X = torch.randn(6, 4, dtype=torch.float32)
    #   W = torch.randn(3, 4, dtype=torch.float32)
    #   b = torch.randn(3, dtype=torch.float32)
    #   out = torch.nn.functional.linear(X, W, b)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    input = np.array(
        [
            [-1.1258398294448853, -1.152360200881958, -0.2505785822868347, -0.4338788092136383],
            [0.8487103581428528, 0.6920091509819031, -0.31601276993751526, -2.1152193546295166],
            [0.46809640526771545, -0.1577124446630478, 1.4436601400375366, 0.26604941487312317],
            [0.16645534336566925, 0.8743818402290344, -0.14347384870052338, -0.1116093322634697],
            [0.9318265914916992, 1.2590092420578003, 2.0049805641174316, 0.05373690277338028],
            [0.6180566549301147, -0.41280221939086914, -0.8410648107528687, -2.316041946411133],
        ],
        dtype=np.float32,
    )
    weight = np.array(
        [
            [0.3703935444355011, 1.4565025568008423, 0.9398099184036255, 0.7748488187789917],
            [0.19186942279338837, 1.2637947797775269, -1.2904350757598877, -0.7911027073860168],
            [-0.02087947353720665, -0.7184800505638123, 0.5186367630958557, -1.3125219345092773],
        ],
        dtype=np.float32,
    )
    bias = np.array(
        [0.1919950693845749, 0.5427713394165039, -2.2187793254852295], dtype=np.float32
    )
    expected = np.array(
        [
            [-2.4751110076904297, -0.4629915952682495, -0.927808403968811],
            [-0.42170220613479614, 3.661320209503174, -0.12131881713867188],
            [1.6985805034637451, -1.6401536464691162, -1.7157001495361328],
            [1.3058699369430542, 1.953186273574829, -2.7784018516540527],
            [4.296826362609863, -0.31711888313293457, -2.1734824180603027],
            [-2.7653515338897705, 3.0572268962860107, 0.6685547828674316],
        ],
        dtype=np.float32,
    )
    result = linear(input, weight, bias)
    assert np.allclose(result, expected, atol=1e-5)
