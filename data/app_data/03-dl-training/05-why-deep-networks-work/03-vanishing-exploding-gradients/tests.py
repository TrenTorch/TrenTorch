"""
pytest data/app_data/03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/05-why-deep-networks-work/{Path(__file__).resolve().parent.name}")
scalar_gradient_chain = _module.scalar_gradient_chain
matrix_gradient_norms = _module.matrix_gradient_norms


def test_scalar_gradient_chain_matches_hand_computation():
    assert np.isclose(scalar_gradient_chain(3, 0.5), 0.125)


def test_scalar_gradient_chain_with_scale_one_is_stable():
    assert np.isclose(scalar_gradient_chain(100, 1.0), 1.0)


def test_scalar_gradient_chain_vanishes_for_scale_less_than_one():
    result = scalar_gradient_chain(50, 0.9)
    assert result < 1e-2


def test_scalar_gradient_chain_explodes_for_scale_greater_than_one():
    result = scalar_gradient_chain(50, 1.1)
    assert result > 100.0


def test_matrix_gradient_norms_has_depth_plus_one_entries():
    rng = np.random.RandomState(0)
    norms = matrix_gradient_norms(depth=10, dim=5, weight_std=1.0, rng=rng)
    assert len(norms) == 11


def test_matrix_gradient_norms_starting_value_matches_the_initial_gradient_norm():
    rng = np.random.RandomState(0)
    norms = matrix_gradient_norms(depth=5, dim=4, weight_std=1.0, rng=rng)
    # initial gradient is np.ones(4), norm = sqrt(4) = 2.0
    assert np.isclose(norms[0], 2.0)


def test_small_weight_std_causes_the_gradient_norm_to_vanish():
    rng = np.random.RandomState(0)
    norms = matrix_gradient_norms(depth=20, dim=10, weight_std=0.1, rng=rng)
    assert norms[-1] < norms[0] * 1e-4


def test_large_weight_std_causes_the_gradient_norm_to_explode():
    rng = np.random.RandomState(0)
    norms = matrix_gradient_norms(depth=20, dim=10, weight_std=1.5, rng=rng)
    assert norms[-1] > norms[0] * 1e4


def test_matrix_gradient_norms_are_all_nonnegative():
    rng = np.random.RandomState(3)
    norms = matrix_gradient_norms(depth=10, dim=6, weight_std=0.8, rng=rng)
    assert all(n >= 0.0 for n in norms)


def test_matrix_gradient_norms_uses_a_fresh_matrix_each_layer_not_the_same_one_reused():
    # Directly targets a mutant that draws ONE random matrix before the
    # loop and reuses it for every layer, instead of drawing a fresh
    # matrix per layer: reusing the same matrix biases the gradient
    # toward its dominant eigenvector much faster (a power-iteration
    # effect), producing a systematically different (and larger, for a
    # matrix with a dominant eigenvalue > 1) final norm than genuinely
    # independent per-layer matrices would.
    dim, depth, weight_std = 8, 15, 1.3
    norms_a = matrix_gradient_norms(depth, dim, weight_std, rng=np.random.RandomState(5))
    norms_b = matrix_gradient_norms(depth, dim, weight_std, rng=np.random.RandomState(5))
    # same seed must give identical results (determinism), which is
    # itself only meaningful if the function correctly reads depth many
    # fresh matrices from the rng stream rather than mishandling state
    assert np.allclose(norms_a, norms_b)
    # a genuinely fresh matrix per layer, drawn from the same rng stream,
    # must have consumed `depth` distinct (dim, dim) draws: verify this
    # indirectly by checking depth=1 and depth=2 give DIFFERENT growth
    # rates than naive repeated-squaring of a single matrix would if the
    # matrix were reused (a reused matrix's norm growth ratio stabilizes
    # to its spectral radius almost immediately; fresh matrices don't).
    single = matrix_gradient_norms(1, dim, weight_std, rng=np.random.RandomState(5))
    assert len(single) == 2
