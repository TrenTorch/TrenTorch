"""
pytest data/app_data/01-classical-ml/01-linear-regression/03-mse-gradient/tests.py

Numbered for the same reason every question in this track is: "Run"
shows the first couple by name, "Submit" runs all of them, and the
numbering keeps both views in the same deliberate order (simple hand-
computed cases first, then shape/bias coverage, edge cases, array
hygiene, mutation-catching cases, then two independent oracles: a
finite-difference numerical gradient check, and a real torch.autograd
reference case).
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

mse_gradient = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).mse_gradient


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_single_sample_single_feature_matches_hand_computation():
    # d(loss)/dw = 2*(pred-target)*input, d(loss)/db = 2*(pred-target),
    # with element_count=1 so the 2/N factor is just 2.
    # pred = 3*2 + 1 = 7, error = 7-5 = 2.
    input = np.array([[3.0]])
    weight = np.array([[2.0]])
    bias = np.array([1.0])
    target = np.array([[5.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert np.allclose(grad_weight, [[12.0]])
    assert np.allclose(grad_bias, [4.0])


def test_02_two_samples_matches_hand_computation():
    # element_count=2 here, so the 1/N factor actually divides by 2 and
    # not 1 -- distinguishes this from a solution that hardcodes N=1.
    input = np.array([[1.0], [2.0]])
    weight = np.array([[3.0]])
    bias = np.array([0.0])
    target = np.array([[0.0], [0.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert np.allclose(grad_weight, [[15.0]])
    assert np.allclose(grad_bias, [9.0])


# --- Shape / bias handling ------------------------------------------------


def test_03_multiple_output_features_returns_weight_shaped_gradient():
    input = np.array([[1.0, 0.0], [0.0, 1.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # out_features=3
    bias = np.array([0.0, 0.0, 0.0])
    target = np.zeros((2, 3))
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert grad_weight.shape == weight.shape
    assert grad_bias.shape == bias.shape


def test_04_bias_none_returns_grad_bias_none():
    # A missing bias parameter has no gradient at all -- not a zero
    # array standing in for it, an actual None, same distinction Q1
    # draws for the forward pass.
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0]])
    target = np.array([[1.0], [1.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, None, target)
    assert grad_bias is None
    assert grad_weight.shape == weight.shape


def test_05_perfect_prediction_gives_zero_gradient():
    # At the minimum of the loss (prediction == target exactly), every
    # gradient must be exactly zero -- there's nowhere left to descend.
    input = np.array([[1.0, -2.0], [0.5, 3.0]])
    weight = np.array([[2.0, -1.0], [0.0, 1.0]])
    bias = np.array([0.5, -0.5])
    prediction = input @ weight.T + bias
    grad_weight, grad_bias = mse_gradient(input, weight, bias, prediction)
    assert np.allclose(grad_weight, 0.0)
    assert np.allclose(grad_bias, 0.0)


# --- Edge cases ------------------------------------------------------------


def test_06_single_sample_batch():
    input = np.array([[2.0, -1.0]])
    weight = np.array([[1.0, 1.0], [0.5, -0.5]])
    bias = np.array([0.0, 0.0])
    target = np.array([[0.0, 0.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert grad_weight.shape == (2, 2)
    assert grad_bias.shape == (2,)


def test_07_over_and_under_predicting_give_opposite_signed_gradients():
    # Symmetric over/under errors of equal magnitude must produce
    # exactly opposite-signed gradients -- the gradient's direction is
    # what a training loop actually steps against, so its sign has to
    # be right, not just its magnitude.
    input = np.array([[1.0]])
    weight = np.array([[1.0]])
    bias = np.array([0.0])
    grad_weight_over, grad_bias_over = mse_gradient(
        input, weight, bias, np.array([[-1.0]])
    )  # prediction=1, target=-1, over-predicting
    grad_weight_under, grad_bias_under = mse_gradient(
        input, weight, bias, np.array([[3.0]])
    )  # prediction=1, target=3, under-predicting
    assert np.allclose(grad_weight_over, -grad_weight_under)
    assert np.allclose(grad_bias_over, -grad_bias_under)


# --- Array hygiene: memory layout and mutability ---------------------------


def test_08_works_on_non_contiguous_arrays():
    base = np.arange(24.0).reshape(4, 6)
    input = base[:, ::2]  # shape (4, 3), non-contiguous
    assert not input.flags["C_CONTIGUOUS"]
    weight = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 1.0]])
    bias = np.array([0.0, 0.0])
    target = np.zeros((4, 2))
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    prediction = input.copy() @ weight.T + bias
    expected_grad_pred = (2.0 / prediction.size) * (prediction - target)
    assert np.allclose(grad_weight, expected_grad_pred.T @ input.copy())
    assert np.allclose(grad_bias, expected_grad_pred.sum(axis=0))


def test_09_does_not_require_writable_inputs():
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    weight = np.array([[1.0, 1.0]])
    bias = np.array([0.5])
    target = np.array([[1.0], [1.0]])
    for arr in (input, weight, bias, target):
        arr.setflags(write=False)
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert grad_weight.shape == (1, 2)
    assert grad_bias.shape == (1,)


def test_10_does_not_mutate_its_inputs():
    input = np.array([[1.0, 2.0]])
    weight = np.array([[1.0, 1.0]])
    bias = np.array([1.0])
    target = np.array([[0.0]])
    input_copy, weight_copy, bias_copy, target_copy = (
        input.copy(),
        weight.copy(),
        bias.copy(),
        target.copy(),
    )
    mse_gradient(input, weight, bias, target)
    assert np.array_equal(input, input_copy)
    assert np.array_equal(weight, weight_copy)
    assert np.array_equal(bias, bias_copy)
    assert np.array_equal(target, target_copy)


# --- Mutation-catching regression cases -------------------------------


def test_11_gradient_scale_factor_is_two_over_element_count():
    # Directly targets two related mutants at once: forgetting the /N
    # (mean vs. sum) and forgetting the factor of 2 from differentiating
    # a square. With batch_size=2, out_features=2 (element_count=4), a
    # "forgot /N" mutant returns 4x too large, a "forgot the 2" mutant
    # returns half as large -- both disagree with the correct 0.5x error
    # scale computed here.
    input = np.array([[1.0], [1.0]])
    weight = np.array([[1.0], [1.0]])  # out_features=2, in_features=1
    bias = np.array([0.0, 0.0])
    target = np.zeros((2, 2))
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert np.allclose(grad_weight, [[1.0], [1.0]])
    assert np.allclose(grad_bias, [1.0, 1.0])


def test_12_weight_gradient_requires_the_correct_transpose_and_axis():
    # Rectangular, non-symmetric weight with in_features != out_features
    # so a dropped/misplaced transpose either crashes on a shape
    # mismatch or produces a shape that isn't weight's shape at all.
    input = np.array([[1.0, 2.0, 3.0]])  # in_features=3
    weight = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])  # out_features=2
    bias = np.array([0.0, 0.0])
    target = np.array([[0.0, 0.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert grad_weight.shape == (2, 3)
    # prediction = [1, 2], error = [1, 2], N=2, grad_pred = [1, 2]
    # grad_weight = grad_pred.T @ input (outer product, since batch=1)
    assert np.allclose(grad_weight, [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]])


def test_13_bias_gradient_sums_over_the_batch_axis_not_the_feature_axis():
    # batch_size != out_features, so summing over the wrong axis either
    # crashes on shape or produces the wrong shape outright.
    input = np.zeros((3, 2))  # weight term contributes nothing
    weight = np.zeros((2, 2))  # out_features=2
    bias = np.array([0.0, 0.0])
    target = np.array([[-1.0, -2.0], [-1.0, -2.0], [-1.0, -2.0]])
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert grad_bias.shape == (2,)
    # prediction is all zero, error = 0 - target = -target everywhere,
    # every row identical, so summing over the batch just triples one row.
    assert np.allclose(grad_bias, (2.0 / 6.0) * 3 * np.array([1.0, 2.0]))


# --- Independent correctness oracles ----------------------------------


def test_14_matches_finite_difference_numerical_gradient():
    # A numerical gradient check doesn't rely on the same chain-rule
    # derivation this function implements at all -- it just directly
    # measures "how much does the loss change when I nudge one number,"
    # which is the actual definition of a gradient. Across several
    # random configurations, since one lucky shape isn't enough to trust.
    def loss_fn(input, weight, bias, target):
        prediction = input @ weight.T
        if bias is not None:
            prediction = prediction + bias
        return float(np.mean((prediction - target) ** 2))

    eps = 1e-5
    configs = [(0, 4, 3, 2), (1, 1, 2, 1), (2, 6, 1, 4), (3, 3, 5, 5)]
    for seed, batch_size, in_features, out_features in configs:
        rng = np.random.default_rng(seed)
        input = rng.normal(size=(batch_size, in_features))
        weight = rng.normal(size=(out_features, in_features))
        bias = rng.normal(size=out_features)
        target = rng.normal(size=(batch_size, out_features))

        analytic_grad_weight, analytic_grad_bias = mse_gradient(input, weight, bias, target)

        numeric_grad_weight = np.zeros_like(weight)
        for i in range(out_features):
            for j in range(in_features):
                perturbed = weight.copy()
                perturbed[i, j] += eps
                loss_plus = loss_fn(input, perturbed, bias, target)
                perturbed[i, j] -= 2 * eps
                loss_minus = loss_fn(input, perturbed, bias, target)
                numeric_grad_weight[i, j] = (loss_plus - loss_minus) / (2 * eps)
        assert np.allclose(
            analytic_grad_weight, numeric_grad_weight, atol=1e-4
        ), f"grad_weight mismatch, seed={seed}"

        numeric_grad_bias = np.zeros_like(bias)
        for i in range(out_features):
            perturbed = bias.copy()
            perturbed[i] += eps
            loss_plus = loss_fn(input, weight, perturbed, target)
            perturbed[i] -= 2 * eps
            loss_minus = loss_fn(input, weight, perturbed, target)
            numeric_grad_bias[i] = (loss_plus - loss_minus) / (2 * eps)
        assert np.allclose(
            analytic_grad_bias, numeric_grad_bias, atol=1e-4
        ), f"grad_bias mismatch, seed={seed}"


def test_15_matches_real_pytorch_autograd_on_a_baked_reference_case():
    # Ground truth from the actual library's automatic differentiation,
    # not our own derivation.
    #
    # Generated once, offline, with:
    #   torch.manual_seed(3)
    #   X = torch.randn(5, 4, dtype=torch.float32)
    #   W = torch.randn(3, 4, dtype=torch.float32, requires_grad=True)
    #   b = torch.randn(3, dtype=torch.float32, requires_grad=True)
    #   Y = torch.randn(5, 3, dtype=torch.float32)
    #   pred = torch.nn.functional.linear(X, W, b)
    #   loss = torch.nn.functional.mse_loss(pred, Y, reduction='mean')
    #   loss.backward()
    #   # W.grad, b.grad are the expected values below
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    input = np.array(
        [
            [-0.07664429396390915, 0.35988152027130127, -0.7820168137550354, 0.07152773439884186],
            [1.0460227727890015, 0.5221869945526123, -0.16680915653705597, 0.05303340032696724],
            [0.4046071469783783, 0.6112996339797974, 0.7603904008865356, -0.03364326059818268],
            [0.997922420501709, 0.45918044447898865, 2.436397075653076, -0.1468081772327423],
            [0.4851140081882477, 0.2052343785762787, 0.33842819929122925, 1.35275399684906],
        ],
        dtype=np.float32,
    )
    weight = np.array(
        [
            [0.49518901109695435, -0.16431698203086853, -0.6779621839523315, -1.0591074228286743],
            [0.7476966381072998, 0.23891741037368774, -0.39215022325515747, 0.15191489458084106],
            [-1.1837332248687744, 0.5343607068061829, -1.451022744178772, -0.6293740272521973],
        ],
        dtype=np.float32,
    )
    bias = np.array(
        [0.154415100812912, -0.24799016118049622, 0.4535011649131775], dtype=np.float32
    )
    target = np.array(
        [
            [0.012091090902686119, 1.3420355319976807, 1.4620037078857422],
            [0.43616098165512085, 1.0170135498046875, -2.1925268173217773],
            [0.2123306691646576, -0.9394968152046204, -0.32357826828956604],
            [-1.054710865020752, 0.8237727284431458, -0.5270501971244812],
            [0.8107258677482605, -0.8045926094055176, -1.050064206123352],
        ],
        dtype=np.float32,
    )
    expected_grad_weight = np.array(
        [
            [-0.11891420185565948, -0.047018278390169144, -0.15367624163627625, -0.37530815601348877],
            [-0.07332849502563477, -0.05588969960808754, -0.11992013454437256, 0.1935243010520935],
            [-0.23581358790397644, -0.104184091091156, -1.2441260814666748, 0.0307118259370327],
        ],
        dtype=np.float32,
    )
    expected_grad_bias = np.array(
        [-0.22817456722259521, -0.11256080865859985, -0.2532424330711365], dtype=np.float32
    )
    grad_weight, grad_bias = mse_gradient(input, weight, bias, target)
    assert np.allclose(grad_weight, expected_grad_weight, atol=1e-5)
    assert np.allclose(grad_bias, expected_grad_bias, atol=1e-5)
