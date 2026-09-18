"""
pytest data/app_data/03-dl-training/01-optimizers/07-gradient-clipping/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
compute_global_norm = _module.compute_global_norm
clip_grad_norm = _module.clip_grad_norm


def test_global_norm_matches_hand_computation():
    grads = [np.array([3.0, 4.0]), np.array([10.0])]
    # sqrt(9+16+100) = sqrt(125)
    assert np.isclose(compute_global_norm(grads), np.sqrt(125.0))


def test_global_norm_matches_known_oracle_from_pytorch():
    grads = [np.array([3.0, 4.0]), np.array([10.0])]
    assert np.isclose(compute_global_norm(grads), 11.180339887498949)


def test_clip_grad_norm_leaves_gradients_unchanged_when_already_under_budget():
    grads = [np.array([1.0, 0.0])]
    result = clip_grad_norm(grads, max_norm=100.0)
    assert np.allclose(result[0], grads[0])


def test_clip_grad_norm_matches_known_oracle_from_pytorch():
    grads = [np.array([3.0, 4.0]), np.array([10.0])]
    result = clip_grad_norm(grads, max_norm=5.0)
    assert np.allclose(result[0], [1.3416407, 1.7888544], atol=1e-6)
    assert np.allclose(result[1], [4.4721356], atol=1e-6)


def test_clip_grad_norm_brings_the_global_norm_down_to_exactly_max_norm():
    grads = [np.array([3.0, 4.0]), np.array([10.0])]
    result = clip_grad_norm(grads, max_norm=5.0)
    new_norm = compute_global_norm(result)
    assert np.isclose(new_norm, 5.0, atol=1e-4)


def test_clip_grad_norm_preserves_relative_proportions_between_gradients():
    grads = [np.array([2.0]), np.array([4.0])]
    result = clip_grad_norm(grads, max_norm=1.0)
    ratio_before = grads[1][0] / grads[0][0]
    ratio_after = result[1][0] / result[0][0]
    assert np.isclose(ratio_before, ratio_after)


def test_clip_grad_norm_returns_copies_not_the_original_arrays():
    grads = [np.array([1.0, 2.0])]
    result = clip_grad_norm(grads, max_norm=100.0)
    result[0][0] = 999.0
    assert grads[0][0] == 1.0  # original must be unaffected


def test_clip_grad_norm_uses_global_norm_not_per_array_norms():
    # Directly targets a mutant that clips each gradient array
    # INDEPENDENTLY (its own separate norm) instead of using one shared
    # global norm across all arrays: this changes the relative scale
    # between arrays in a way a correct global-norm clip never would.
    grads = [np.array([3.0, 4.0]), np.array([0.1])]  # first array dominates the global norm
    result = clip_grad_norm(grads, max_norm=1.0)
    # Correct global clip: both scaled by the SAME factor (max_norm / global_norm).
    global_norm = compute_global_norm(grads)
    expected_coef = 1.0 / global_norm
    assert np.allclose(result[0], grads[0] * expected_coef, atol=1e-6)
    assert np.allclose(result[1], grads[1] * expected_coef, atol=1e-6)
