"""
pytest data/app_data/01-classical-ml/01-linear-regression/02-mse-loss/tests.py

Numbered for the same reason 01-hypothesis-function's are: "Run" shows
the first couple by name, "Submit" runs all of them, and the numbering
keeps both in one deliberate order (simple cases, then each reduction
mode, edge cases, array hygiene, mutation-catching cases, then two
independent oracles).
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_loss = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).mse_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_mean_reduction_matches_hand_computation():
    # errors are 1, 4, 9 -- mean is 14/3.
    input = np.array([1.0, 2.0, 3.0])
    target = np.array([2.0, 4.0, 6.0])
    assert np.isclose(mse_loss(input, target), 14.0 / 3.0)


def test_02_sum_reduction_matches_hand_computation():
    # Same errors as above, but summed instead of averaged: 1+4+9=14.
    input = np.array([1.0, 2.0, 3.0])
    target = np.array([2.0, 4.0, 6.0])
    assert np.isclose(mse_loss(input, target, reduction="sum"), 14.0)


# --- Each reduction mode ------------------------------------------------


def test_03_none_reduction_preserves_shape_and_values():
    # 'none' skips reduction entirely: every squared error comes back,
    # same shape as the input, nothing averaged or summed away.
    input = np.array([1.0, 2.0, 3.0])
    target = np.array([2.0, 4.0, 6.0])
    result = mse_loss(input, target, reduction="none")
    assert result.shape == (3,)
    assert np.allclose(result, [1.0, 4.0, 9.0])


def test_04_default_reduction_is_mean():
    # Calling without a third argument must behave identically to an
    # explicit reduction="mean" -- the default has to actually be wired
    # up, not just documented.
    input = np.array([1.0, -2.0, 3.5])
    target = np.array([0.0, 0.0, 0.0])
    assert mse_loss(input, target) == mse_loss(input, target, reduction="mean")


def test_05_invalid_reduction_raises():
    input = np.array([1.0, 2.0])
    target = np.array([1.0, 2.0])
    try:
        mse_loss(input, target, reduction="average")
        assert False, "expected a ValueError for an unrecognized reduction"
    except ValueError:
        pass


# --- Edge cases ----------------------------------------------------------


def test_06_zero_loss_when_prediction_matches_target_exactly():
    input = np.array([1.0, -2.5, 0.0, 100.0])
    target = input.copy()
    assert mse_loss(input, target) == 0.0
    assert mse_loss(input, target, reduction="sum") == 0.0
    assert np.allclose(mse_loss(input, target, reduction="none"), 0.0)


def test_07_multi_dimensional_input_reduces_over_every_element():
    # This function has to work on the (batch_size, out_features) shape
    # 01-hypothesis-function's `linear` actually produces, not just 1-D
    # vectors. mean/sum reduce over the whole array, not per row.
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    target = np.array([[0.0, 0.0], [0.0, 0.0]])
    # errors: 1, 4, 9, 16 -- mean = 30/4 = 7.5, sum = 30.
    assert np.isclose(mse_loss(input, target), 7.5)
    assert np.isclose(mse_loss(input, target, reduction="sum"), 30.0)
    none_result = mse_loss(input, target, reduction="none")
    assert none_result.shape == (2, 2)
    assert np.allclose(none_result, [[1.0, 4.0], [9.0, 16.0]])


def test_08_sign_of_the_error_never_matters():
    # A prediction 2 too high and one 2 too low contribute the same
    # squared error -- a solution that quietly uses abs() somewhere
    # instead of squaring would still pass simpler tests but not this
    # asymmetric pairing.
    over = mse_loss(np.array([5.0]), np.array([3.0]))
    under = mse_loss(np.array([1.0]), np.array([3.0]))
    assert np.isclose(over, under)


def test_09_return_types_match_reduction():
    # 'mean'/'sum' return a plain Python float (a scalar loss you can
    # print or log directly); 'none' returns an ndarray. Mixing these up
    # is a real, easy-to-make bug.
    input = np.array([1.0, 2.0])
    target = np.array([1.5, 2.5])
    assert isinstance(mse_loss(input, target), float)
    assert isinstance(mse_loss(input, target, reduction="sum"), float)
    assert isinstance(mse_loss(input, target, reduction="none"), np.ndarray)


# --- Array hygiene: memory layout and mutability ---------------------


def test_10_works_on_non_contiguous_arrays():
    base = np.arange(12.0).reshape(4, 3)
    input = base[:, ::2]  # shape (4, 2), non-contiguous
    assert not input.flags["C_CONTIGUOUS"]
    target = np.zeros_like(input)
    assert np.isclose(mse_loss(input, target), np.mean(input.copy() ** 2))


def test_11_does_not_require_writable_inputs():
    input = np.array([1.0, 2.0, 3.0])
    target = np.array([1.0, 1.0, 1.0])
    for arr in (input, target):
        arr.setflags(write=False)
    assert np.isclose(mse_loss(input, target), 5.0 / 3.0)


def test_12_does_not_mutate_its_inputs():
    input = np.array([1.0, 2.0, 3.0])
    target = np.array([0.0, 0.0, 0.0])
    input_copy, target_copy = input.copy(), target.copy()
    mse_loss(input, target, reduction="none")
    assert np.array_equal(input, input_copy)
    assert np.array_equal(target, target_copy)


# --- Mutation-catching regression cases -------------------------------


def test_13_squares_the_error_not_absolute_value():
    # Directly targets the "used abs() instead of **2" mutant. Errors of
    # 1 and 3 give mean-of-squares 5.0 but mean-of-abs 2.0 -- the two are
    # only ever equal when every error has magnitude 0 or 1.
    input = np.array([2.0, 6.0])
    target = np.array([1.0, 3.0])
    assert np.isclose(mse_loss(input, target), 5.0)


def test_14_mean_actually_divides_by_element_count():
    # Directly targets a "returns sum when asked for mean" mutant, or a
    # mean computed over the wrong axis/count. 10 elements, all with
    # squared error 4, must give mean 4.0, not 40.0 or something per-row.
    input = np.full((2, 5), 2.0)
    target = np.zeros((2, 5))
    assert np.isclose(mse_loss(input, target), 4.0)


# --- Independent correctness oracles ----------------------------------


def test_15_matches_manual_computation_across_several_random_shapes():
    configs = [(0, (200,)), (1, (5, 4)), (2, (1, 10)), (3, (17, 3))]
    for seed, shape in configs:
        rng = np.random.default_rng(seed)
        input = rng.normal(size=shape)
        target = rng.normal(size=shape)
        manual_mean = float(np.sum((input - target) ** 2) / input.size)
        manual_sum = float(np.sum((input - target) ** 2))
        assert np.isclose(mse_loss(input, target), manual_mean), f"mean mismatch, shape={shape}"
        assert np.isclose(
            mse_loss(input, target, reduction="sum"), manual_sum
        ), f"sum mismatch, shape={shape}"
        assert np.allclose(
            mse_loss(input, target, reduction="none"), (input - target) ** 2
        ), f"none mismatch, shape={shape}"


def test_16_matches_real_pytorch_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(7)
    #   X = torch.randn(5, 3, dtype=torch.float32)
    #   Y = torch.randn(5, 3, dtype=torch.float32)
    #   mean = F.mse_loss(X, Y, reduction='mean')
    #   total = F.mse_loss(X, Y, reduction='sum')
    #   none = F.mse_loss(X, Y, reduction='none')
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    input = np.array(
        [
            [-0.1467950940132141, 0.7861412763595581, 0.9468216300010681],
            [-1.1143440008163452, 1.6907901763916016, -0.8948279023170471],
            [-0.3556250333786011, 1.2323857545852661, 0.13817265629768372],
            [-1.6821985244750977, 0.317678302526474, 0.13280697166919708],
            [0.13732409477233887, 0.2405461221933365, 1.3954508304595947],
        ],
        dtype=np.float32,
    )
    target = np.array(
        [
            [1.3470226526260376, 2.4382081031799316, 0.2027582824230194],
            [2.4505412578582764, 2.025601863861084, 1.7791550159454346],
            [-0.9179307222366333, -0.4578188955783844, -0.7244732975959778],
            [1.2798781394958496, -0.9940662384033203, 1.8149727582931519],
            [-0.6028482913970947, 1.6148147583007812, 1.9301981925964355],
        ],
        dtype=np.float32,
    )
    expected_none = np.array(
        [
            [2.2314915657043457, 2.7293248176574707, 0.5536302924156189],
            [12.708406448364258, 0.11209886521100998, 7.150184154510498],
            [0.31618767976760864, 2.8567917346954346, 0.7441580891609192],
            [8.773898124694824, 1.7206737995147705, 2.829681634902954],
            [0.5478551387786865, 1.888614296913147, 0.2859547436237335],
        ],
        dtype=np.float32,
    )
    assert np.isclose(mse_loss(input, target, reduction="mean"), 3.0299301147460938, atol=1e-4)
    assert np.isclose(mse_loss(input, target, reduction="sum"), 45.448951721191406, atol=1e-3)
    assert np.allclose(mse_loss(input, target, reduction="none"), expected_none, atol=1e-4)
