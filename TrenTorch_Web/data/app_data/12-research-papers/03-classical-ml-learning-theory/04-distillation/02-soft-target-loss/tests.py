"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/04-distillation/02-soft-target-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-distill-soft-target-ce")
soft_target_ce = _module.soft_target_ce


import numpy as np


def test_1_identical_logits_give_entropy_times_t_squared():
    # Uniform over 2 classes: entropy = log 2. With T = 2 the loss is 4 * log 2.
    out = soft_target_ce(np.zeros(2), np.zeros(2), 2.0)
    assert abs(out - 4 * np.log(2.0)) < 1e-9


def test_2_loss_is_nonnegative():
    assert soft_target_ce(np.array([1.0, 0.0, -1.0]), np.array([0.0, 0.0, 0.0]), 1.0) >= 0


def test_3_matching_student_has_lower_loss_than_mismatched():
    teacher = np.array([3.0, 0.0])
    good = soft_target_ce(teacher, np.array([3.0, 0.0]), 1.0)
    bad = soft_target_ce(teacher, np.array([0.0, 3.0]), 1.0)
    assert bad > good


def test_4_returns_a_python_float():
    assert isinstance(soft_target_ce(np.zeros(3), np.zeros(3), 1.0), float)


def test_5_larger_temperature_scales_the_loss_by_t_squared_at_uniform():
    a = soft_target_ce(np.zeros(2), np.zeros(2), 1.0)
    b = soft_target_ce(np.zeros(2), np.zeros(2), 3.0)
    assert abs(b - 9 * a) < 1e-9


def test_6_does_not_mutate_inputs():
    t = np.array([1.0, 2.0])
    soft_target_ce(t, np.array([0.0, 0.0]), 2.0)
    np.testing.assert_array_equal(t, [1.0, 2.0])

