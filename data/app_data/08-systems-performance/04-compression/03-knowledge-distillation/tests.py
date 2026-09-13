"""
pytest data/app_data/08-systems-performance/04-compression/03-knowledge-distillation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

distillation_loss = load_solution(
    f"08-systems-performance/04-compression/{Path(__file__).resolve().parent.name}"
).distillation_loss
cce_loss = load_solution("01-classical-ml/02-classification/06-softmax-cce").cce_loss
softmax = load_solution("01-classical-ml/02-classification/06-softmax-cce").softmax


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_returns_a_plain_positive_float():
    rng = np.random.default_rng(0)
    student = rng.normal(size=(4, 3))
    teacher = rng.normal(size=(4, 3))
    labels = np.array([0, 1, 2, 0])
    loss = distillation_loss(student, teacher, labels)
    assert isinstance(loss, float)
    assert loss > 0.0


def test_02_identical_student_and_teacher_gives_zero_soft_loss_component():
    # If student and teacher logits are identical, the KL divergence
    # between their softened distributions is exactly 0 -- only the
    # hard loss contributes.
    rng = np.random.default_rng(1)
    logits = rng.normal(size=(4, 3))
    labels = np.array([0, 1, 2, 0])
    loss_alpha_1 = distillation_loss(logits, logits, labels, alpha=1.0)
    assert np.isclose(loss_alpha_1, 0.0, atol=1e-8)


# --- Shape / general-case coverage -----------------------------------


def test_03_alpha_zero_reduces_to_pure_hard_label_cross_entropy():
    rng = np.random.default_rng(2)
    student = rng.normal(size=(5, 4))
    teacher = rng.normal(size=(5, 4))
    labels = np.array([0, 1, 2, 3, 0])
    loss = distillation_loss(student, teacher, labels, alpha=0.0)
    expected = cce_loss(softmax(student), labels)
    assert np.isclose(loss, expected)


def test_04_higher_temperature_changes_the_soft_loss_value():
    rng = np.random.default_rng(3)
    student = rng.normal(scale=3.0, size=(4, 3))
    teacher = rng.normal(scale=3.0, size=(4, 3))
    labels = np.array([0, 1, 2, 0])
    loss_low_temp = distillation_loss(student, teacher, labels, temperature=1.0, alpha=1.0)
    loss_high_temp = distillation_loss(student, teacher, labels, temperature=4.0, alpha=1.0)
    assert not np.isclose(loss_low_temp, loss_high_temp)


# --- Parameter handling -------------------------------------------------


def test_05_alpha_interpolates_between_soft_and_hard_loss():
    rng = np.random.default_rng(4)
    student = rng.normal(size=(4, 3))
    teacher = rng.normal(size=(4, 3))
    labels = np.array([0, 1, 2, 0])
    loss_soft_only = distillation_loss(student, teacher, labels, alpha=1.0)
    loss_hard_only = distillation_loss(student, teacher, labels, alpha=0.0)
    loss_half = distillation_loss(student, teacher, labels, alpha=0.5)
    assert np.isclose(loss_half, 0.5 * loss_soft_only + 0.5 * loss_hard_only)


# --- Edge cases ---------------------------------------------------------


def test_06_single_sample_batch_works():
    student = np.array([[1.0, 0.5, -0.5]])
    teacher = np.array([[0.8, 0.6, -0.4]])
    labels = np.array([0])
    loss = distillation_loss(student, teacher, labels)
    assert np.isfinite(loss)


def test_07_binary_classification_works():
    rng = np.random.default_rng(5)
    student = rng.normal(size=(6, 2))
    teacher = rng.normal(size=(6, 2))
    labels = rng.integers(0, 2, size=6)
    loss = distillation_loss(student, teacher, labels)
    assert np.isfinite(loss)


# --- Array hygiene ------------------------------------------------------


def test_08_does_not_mutate_its_inputs():
    student = np.array([[1.0, 0.0]])
    teacher = np.array([[0.5, 0.5]])
    student_copy, teacher_copy = student.copy(), teacher.copy()
    distillation_loss(student, teacher, np.array([0]))
    assert np.array_equal(student, student_copy)
    assert np.array_equal(teacher, teacher_copy)


# --- Independent correctness oracle -----------------------------------


def test_09_matches_real_pytorch_hinton_distillation_loss_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(0)
    #   student_logits = rng.normal(size=(4, 3))
    #   teacher_logits = rng.normal(size=(4, 3))
    #   labels = torch.tensor([0, 1, 2, 0])
    #   T = 2.0
    #   soft_loss = F.kl_div(
    #       F.log_softmax(torch.tensor(student_logits) / T, dim=1),
    #       F.softmax(torch.tensor(teacher_logits) / T, dim=1),
    #       reduction="batchmean",
    #   ) * T * T
    #   hard_loss = F.cross_entropy(torch.tensor(student_logits), labels)
    #   total = 0.5 * soft_loss + 0.5 * hard_loss  # 1.1106041946788827
    #
    # This test needs no torch installed to run.
    rng = np.random.default_rng(0)
    student_logits = rng.normal(size=(4, 3))
    teacher_logits = rng.normal(size=(4, 3))
    labels = np.array([0, 1, 2, 0])
    expected_loss = 1.1106041946788827

    loss = distillation_loss(student_logits, teacher_logits, labels, temperature=2.0, alpha=0.5)
    assert np.isclose(loss, expected_loss, atol=1e-6)
