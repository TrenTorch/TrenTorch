"""
pytest data/app_data/03-dl-training/02-layers/03-dropout/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
dropout_forward = _module.dropout_forward
dropout_backward = _module.dropout_backward


def test_dropped_entries_are_exactly_zero():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    mask = np.array([1.0, 0.0, 1.0, 0.0])
    result = dropout_forward(x, mask, p=0.5)
    assert result[1] == 0.0
    assert result[3] == 0.0


def test_kept_entries_are_scaled_by_one_over_one_minus_p():
    x = np.array([1.0, 1.0, 1.0, 1.0])
    mask = np.array([1.0, 1.0, 1.0, 1.0])
    result = dropout_forward(x, mask, p=0.25)
    assert np.allclose(result, 4.0 / 3.0)


def test_hand_computed_forward_example():
    x = np.array([2.0, 4.0, 6.0])
    mask = np.array([1.0, 0.0, 1.0])
    result = dropout_forward(x, mask, p=0.5)
    # survivors scaled by 1/(1-0.5) = 2: 2*2=4, dropped: 0, 6*2=12
    assert np.allclose(result, [4.0, 0.0, 12.0])


def test_p_equals_zero_leaves_input_unchanged_when_mask_is_all_ones():
    x = np.array([1.0, 2.0, 3.0])
    mask = np.array([1.0, 1.0, 1.0])
    result = dropout_forward(x, mask, p=0.0)
    assert np.allclose(result, x)


def test_backward_zeroes_gradient_at_dropped_positions():
    grad_output = np.array([1.0, 1.0, 1.0, 1.0])
    mask = np.array([1.0, 0.0, 1.0, 0.0])
    result = dropout_backward(grad_output, mask, p=0.5)
    assert result[1] == 0.0
    assert result[3] == 0.0


def test_backward_uses_the_same_scaling_as_forward():
    grad_output = np.array([1.0, 1.0])
    mask = np.array([1.0, 1.0])
    result = dropout_backward(grad_output, mask, p=0.25)
    assert np.allclose(result, 4.0 / 3.0)


def test_forward_and_backward_apply_the_identical_transformation():
    # Since dropout is a per-entry multiply by a fixed constant, applying
    # dropout_forward to any array must give the same result as
    # dropout_backward on that same array, for the same mask and p.
    values = np.array([1.5, -2.0, 3.25, 0.0])
    mask = np.array([1.0, 0.0, 1.0, 1.0])
    p = 0.4
    assert np.allclose(dropout_forward(values, mask, p), dropout_backward(values, mask, p))


def test_matches_known_oracle_from_pytorch_inverted_dropout_convention():
    # Verified against torch.nn.functional.dropout's scaling convention:
    # surviving entries are exactly x / (1 - p), not x unscaled.
    x = np.array([1.0])
    mask = np.array([1.0])
    result = dropout_forward(x, mask, p=0.3)
    assert np.isclose(result[0], 1.0 / 0.7)


def test_does_not_forget_the_rescale_divides_not_multiplies_by_keep_prob():
    # Directly targets a mutant that multiplies by (1 - p) instead of
    # dividing by it (a plausible sign-of-operation slip): for p=0.5 this
    # produces 0.5x instead of the correct 2x.
    x = np.array([1.0])
    mask = np.array([1.0])
    result = dropout_forward(x, mask, p=0.5)
    assert np.isclose(result[0], 2.0)
