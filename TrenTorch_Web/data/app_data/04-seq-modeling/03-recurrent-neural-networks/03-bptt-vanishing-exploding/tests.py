"""
pytest data/app_data/04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/03-recurrent-neural-networks/{Path(__file__).resolve().parent.name}")
bptt_gradient_norms = _module.bptt_gradient_norms


def test_returns_seq_len_plus_one_norms():
    weight_hh = np.eye(4)
    grad_final = np.ones(4)
    norms = bptt_gradient_norms(seq_len=10, weight_hh=weight_hh, grad_h_final=grad_final)
    assert len(norms) == 11


def test_starting_norm_matches_the_initial_gradient():
    weight_hh = np.eye(3)
    grad_final = np.array([3.0, 4.0, 0.0])
    norms = bptt_gradient_norms(seq_len=5, weight_hh=weight_hh, grad_h_final=grad_final)
    assert np.isclose(norms[0], 5.0)


def test_identity_matrix_leaves_norm_unchanged_across_all_steps():
    weight_hh = np.eye(4)
    grad_final = np.array([1.0, 2.0, 3.0, 4.0])
    norms = bptt_gradient_norms(seq_len=20, weight_hh=weight_hh, grad_h_final=grad_final)
    expected_norm = np.linalg.norm(grad_final)
    for n in norms:
        assert np.isclose(n, expected_norm)


def test_small_scale_weight_causes_the_norm_to_vanish():
    rng = np.random.RandomState(0)
    weight_hh = rng.randn(6, 6) * 0.1
    grad_final = np.ones(6)
    norms = bptt_gradient_norms(seq_len=30, weight_hh=weight_hh, grad_h_final=grad_final)
    assert norms[-1] < norms[0] * 1e-6


def test_large_scale_weight_causes_the_norm_to_explode():
    rng = np.random.RandomState(0)
    weight_hh = rng.randn(6, 6) * 0.5
    grad_final = np.ones(6)
    norms = bptt_gradient_norms(seq_len=30, weight_hh=weight_hh, grad_h_final=grad_final)
    assert norms[-1] > norms[0] * 1e3


def test_all_norms_are_nonnegative():
    rng = np.random.RandomState(1)
    weight_hh = rng.randn(5, 5) * 0.3
    grad_final = rng.randn(5)
    norms = bptt_gradient_norms(seq_len=15, weight_hh=weight_hh, grad_h_final=grad_final)
    assert all(n >= 0.0 for n in norms)


def test_reuses_the_same_matrix_every_step_not_a_fresh_one():
    # Directly targets a mutant that (incorrectly, for THIS specific
    # question's point) draws a fresh random matrix every step instead
    # of reusing the same weight_hh: with the SAME seed and the SAME
    # weight_hh reused correctly, two independent calls must produce
    # IDENTICAL results (no hidden randomness anywhere in a correct
    # implementation, since weight_hh and grad_h_final are both fixed,
    # deterministic inputs).
    weight_hh = np.array([[1.2, 0.0], [0.0, 0.8]])
    grad_final = np.array([1.0, 1.0])
    norms_a = bptt_gradient_norms(seq_len=10, weight_hh=weight_hh, grad_h_final=grad_final)
    norms_b = bptt_gradient_norms(seq_len=10, weight_hh=weight_hh, grad_h_final=grad_final)
    assert norms_a == norms_b
