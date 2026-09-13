"""
pytest data/app_data/10-rl-alignment/03-fine-tuning/03-kl-divergence-distillation-rlhf-penalty/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/03-fine-tuning/{Path(__file__).resolve().parent.name}")
distillation_loss = _module.distillation_loss
rlhf_kl_penalty = _module.rlhf_kl_penalty
kl_divergence = _module.kl_divergence


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_distillation_loss_is_zero_for_identical_distributions():
    dist = np.array([[0.5, 0.3, 0.2], [0.1, 0.8, 0.1]])
    assert math.isclose(distillation_loss(dist, dist), 0.0, abs_tol=1e-9)


def test_02_rlhf_kl_penalty_zero_when_policy_matches_reference():
    dist = np.array([[0.4, 0.4, 0.2]])
    assert math.isclose(rlhf_kl_penalty(dist, dist, beta=0.1), 0.0, abs_tol=1e-9)


# --- General-case coverage --------------------------------------------


def test_03_distillation_loss_grows_as_student_diverges_from_teacher():
    teacher = np.array([[0.7, 0.2, 0.1]])
    close_student = np.array([[0.65, 0.25, 0.1]])
    far_student = np.array([[0.1, 0.1, 0.8]])
    assert distillation_loss(teacher, close_student) < distillation_loss(teacher, far_student)


def test_04_distillation_loss_matches_manual_batch_average():
    teacher = np.array([[0.7, 0.3], [0.4, 0.6]])
    student = np.array([[0.6, 0.4], [0.5, 0.5]])
    manual = np.mean([kl_divergence(teacher[i], student[i], base=np.e) for i in range(2)])
    assert math.isclose(distillation_loss(teacher, student), manual)


def test_05_rlhf_kl_penalty_scales_linearly_with_beta():
    policy = np.array([[0.9, 0.05, 0.05]])
    reference = np.array([[0.5, 0.3, 0.2]])
    penalty_small = rlhf_kl_penalty(policy, reference, beta=0.1)
    penalty_large = rlhf_kl_penalty(policy, reference, beta=0.4)
    assert math.isclose(penalty_large, 4 * penalty_small)


# --- Parameter handling -------------------------------------------------


def test_06_distillation_loss_is_asymmetric():
    # A symmetric [a, 1-a] vs [1-a, a] pair happens to give equal KL in
    # both directions by pure mirror-symmetry -- use a genuinely
    # lopsided pair instead, where the two directions truly diverge.
    p = np.array([[0.9, 0.05, 0.05]])
    q = np.array([[0.4, 0.4, 0.2]])
    # KL(p||q) != KL(q||p) in general -- the direction genuinely matters.
    assert not math.isclose(distillation_loss(p, q), distillation_loss(q, p))


def test_07_works_across_a_multi_row_batch():
    teacher = np.array([[0.5, 0.5], [0.2, 0.8], [0.9, 0.1]])
    student = np.array([[0.5, 0.5], [0.3, 0.7], [0.6, 0.4]])
    result = distillation_loss(teacher, student)
    assert result > 0.0


# --- Edge cases ---------------------------------------------------------


def test_08_single_row_batch():
    teacher = np.array([[0.6, 0.4]])
    student = np.array([[0.5, 0.5]])
    result = distillation_loss(teacher, student)
    assert math.isclose(result, kl_divergence(teacher[0], student[0], base=np.e))


def test_09_zero_beta_gives_zero_penalty_regardless_of_divergence():
    policy = np.array([[0.99, 0.01]])
    reference = np.array([[0.01, 0.99]])
    assert math.isclose(rlhf_kl_penalty(policy, reference, beta=0.0), 0.0)


# --- Independent correctness oracle -----------------------------------


def test_10_both_functions_reduce_to_the_same_underlying_kl_formula():
    # Directly targets a mutant that reimplements KL divergence from
    # scratch (incorrectly) instead of reusing math-kl-divergence's
    # already-verified kl_divergence -- both distillation_loss and
    # rlhf_kl_penalty (with beta=1) on the SAME pair of distributions
    # must agree with each other AND with a direct kl_divergence call.
    a = np.array([[0.6, 0.3, 0.1]])
    b = np.array([[0.3, 0.3, 0.4]])
    expected = kl_divergence(a[0], b[0], base=np.e)
    assert math.isclose(distillation_loss(a, b), expected)
    assert math.isclose(rlhf_kl_penalty(a, b, beta=1.0), expected)
