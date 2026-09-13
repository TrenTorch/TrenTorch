"""
pytest data/app_data/08-systems-performance/03-mixed-precision-training/02-loss-scaling/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"08-systems-performance/03-mixed-precision-training/{Path(__file__).resolve().parent.name}")
scale_loss = _module.scale_loss
unscale_gradients = _module.unscale_gradients
has_inf_or_nan = _module.has_inf_or_nan


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_scale_loss_matches_hand_computation():
    assert scale_loss(0.5, 1024.0) == 512.0


def test_02_unscale_gradients_matches_hand_computation():
    grads = [np.array([1024.0, 2048.0])]
    result = unscale_gradients(grads, 1024.0)
    assert np.allclose(result[0], [1.0, 2.0])


# --- Shape / general-case coverage -----------------------------------


def test_03_unscale_handles_multiple_gradient_arrays():
    grads = [np.array([512.0]), np.array([[1024.0, 2048.0]])]
    result = unscale_gradients(grads, 512.0)
    assert np.allclose(result[0], [1.0])
    assert np.allclose(result[1], [[2.0, 4.0]])


def test_04_scale_then_unscale_round_trips_a_realistic_small_gradient():
    # The actual point of loss scaling: a gradient of 1e-6, scaled by
    # 65536 before backward, then unscaled by the same factor after,
    # should recover very close to the original value -- and crucially,
    # never touch fp16's underflow floor along the way (checked in
    # 01-fp16-bf16-representable-range).
    scale = 65536.0
    original_grad = 1e-6
    scaled_grad = original_grad * scale  # what a real scaled backward pass would produce
    unscaled = unscale_gradients([np.array([scaled_grad])], scale)
    assert np.isclose(unscaled[0][0], original_grad, rtol=1e-4)


# --- Parameter handling -------------------------------------------------


def test_05_has_inf_or_nan_detects_inf():
    grads = [np.array([1.0, np.inf])]
    assert has_inf_or_nan(grads) is True


def test_06_has_inf_or_nan_detects_nan():
    grads = [np.array([1.0, np.nan])]
    assert has_inf_or_nan(grads) is True


def test_07_has_inf_or_nan_is_false_for_all_finite_gradients():
    grads = [np.array([1.0, 2.0]), np.array([-3.0])]
    assert has_inf_or_nan(grads) is False


def test_08_has_inf_or_nan_checks_every_array_not_just_the_first():
    grads = [np.array([1.0, 2.0]), np.array([np.inf])]
    assert has_inf_or_nan(grads) is True


# --- Edge cases ---------------------------------------------------------


def test_09_empty_gradient_list_has_no_inf_or_nan():
    assert has_inf_or_nan([]) is False


def test_10_scale_of_one_is_the_identity_for_both_operations():
    assert scale_loss(3.5, 1.0) == 3.5
    grads = [np.array([1.0, 2.0])]
    result = unscale_gradients(grads, 1.0)
    assert np.array_equal(result[0], grads[0])


# --- Array hygiene ------------------------------------------------------


def test_11_unscale_does_not_mutate_the_input_gradient_arrays():
    grads = [np.array([100.0])]
    grads_copy = [g.copy() for g in grads]
    unscale_gradients(grads, 100.0)
    assert np.array_equal(grads[0], grads_copy[0])


# --- Independent correctness oracle -----------------------------------


def test_12_dynamic_loss_scaling_workflow_matches_the_real_amp_pattern():
    # This is the exact loop structure torch.cuda.amp.GradScaler
    # implements internally: scale the loss, run backward, check for
    # inf/nan BEFORE unscaling (an overflowed gradient would already be
    # inf regardless of the unscale step), skip the optimizer step and
    # shrink `scale` if anything overflowed, otherwise unscale and step
    # normally.
    scale = 2.0**16

    def fake_backward_pass(scaled_loss_multiplier):
        # simulates a backward pass whose "raw" per-parameter gradient
        # is 1e-5, scaled up by whatever the loss was scaled by
        return [np.array([1e-5]) * scaled_loss_multiplier]

    scaled_loss = scale_loss(0.1, scale)
    raw_grads = fake_backward_pass(scale)

    if has_inf_or_nan(raw_grads):
        step_taken = False
    else:
        _ = unscale_gradients(raw_grads, scale)
        step_taken = True

    assert step_taken is True
    assert scaled_loss == 0.1 * scale
