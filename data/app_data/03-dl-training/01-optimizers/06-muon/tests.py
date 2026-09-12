"""
pytest data/app_data/03-dl-training/01-optimizers/06-muon/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
newton_schulz_orthogonalize = _module.newton_schulz_orthogonalize
muon_step = _module.muon_step


def test_newton_schulz_preserves_shape_for_square_matrix():
    rng = np.random.default_rng(0)
    g = rng.normal(size=(5, 5))
    result = newton_schulz_orthogonalize(g)
    assert result.shape == (5, 5)


def test_newton_schulz_preserves_shape_for_tall_matrix():
    rng = np.random.default_rng(1)
    g = rng.normal(size=(9, 4))
    result = newton_schulz_orthogonalize(g)
    assert result.shape == (9, 4)


def test_newton_schulz_preserves_shape_for_wide_matrix():
    rng = np.random.default_rng(2)
    g = rng.normal(size=(4, 9))
    result = newton_schulz_orthogonalize(g)
    assert result.shape == (4, 9)


def test_newton_schulz_pushes_singular_values_closer_to_one():
    # The core, verifiable property: singular values end up SUBSTANTIALLY
    # closer to 1 than before, even though the iteration does not fully
    # converge to exact orthogonality in a handful of steps.
    rng = np.random.default_rng(3)
    g = rng.normal(size=(6, 6))
    normalized = g / np.linalg.norm(g)
    before_sv = np.linalg.svd(normalized, compute_uv=False)

    result = newton_schulz_orthogonalize(g)
    after_sv = np.linalg.svd(result, compute_uv=False)

    distance_before = np.mean(np.abs(before_sv - 1.0))
    distance_after = np.mean(np.abs(after_sv - 1.0))
    assert distance_after < distance_before * 0.5


def test_newton_schulz_result_is_finite():
    rng = np.random.default_rng(4)
    g = rng.normal(size=(7, 3)) * 100.0  # large-magnitude input
    result = newton_schulz_orthogonalize(g)
    assert np.all(np.isfinite(result))


def test_newton_schulz_more_steps_gets_at_least_as_close_on_average():
    rng = np.random.default_rng(5)
    g = rng.normal(size=(5, 5))
    few_steps = newton_schulz_orthogonalize(g, steps=1)
    more_steps = newton_schulz_orthogonalize(g, steps=5)
    sv_few = np.linalg.svd(few_steps, compute_uv=False)
    sv_more = np.linalg.svd(more_steps, compute_uv=False)
    assert np.mean(np.abs(sv_more - 1.0)) < np.mean(np.abs(sv_few - 1.0))


def test_muon_step_accumulates_momentum_correctly():
    param = np.zeros((3, 3))
    grad = np.eye(3)
    momentum_buf = np.zeros((3, 3))
    _, new_buf = muon_step(param, grad, momentum_buf, lr=0.01, momentum=0.9)
    assert np.allclose(new_buf, grad)  # 0.9*0 + grad = grad


def test_muon_step_changes_the_parameter():
    rng = np.random.default_rng(6)
    param = rng.normal(size=(4, 4))
    grad = rng.normal(size=(4, 4))
    momentum_buf = np.zeros((4, 4))
    new_param, _ = muon_step(param, grad, momentum_buf, lr=0.1, momentum=0.95)
    assert not np.allclose(param, new_param)


def test_muon_step_orthogonalizes_the_momentum_not_the_raw_gradient():
    # Directly targets a mutant that orthogonalizes `grad` directly,
    # bypassing momentum accumulation entirely. With a nonzero prior
    # momentum buffer, the correct update must reflect BOTH the prior
    # buffer and the new gradient, not the gradient alone.
    param = np.zeros((3, 3))
    grad = np.zeros((3, 3))  # zero current gradient
    momentum_buf = np.eye(3) * 5.0  # large prior momentum
    new_param, new_buf = muon_step(param, grad, momentum_buf, lr=0.1, momentum=0.9)
    # new_buf = 0.9*5*I + 0 = 4.5*I, nonzero -> update must be nonzero
    assert not np.allclose(new_param, param)
    assert np.allclose(new_buf, np.eye(3) * 4.5)
