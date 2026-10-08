"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/05-rethinking-generalization/02-generalization-gap/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-generalization-gap")
generalization_gap = _module.generalization_gap


def test_1_matches_a_hand_value():
    assert abs(generalization_gap(1.0, 0.6) - 0.4) < 1e-12


def test_2_equal_accuracies_give_zero_gap():
    assert generalization_gap(0.8, 0.8) == 0.0


def test_3_memorizing_model_has_a_large_gap():
    assert generalization_gap(1.0, 0.1) > 0.8


def test_4_gap_can_be_negative():
    assert generalization_gap(0.5, 0.7) < 0


def test_5_returns_a_float_for_floats():
    assert isinstance(generalization_gap(0.9, 0.5), float)


def test_6_is_antisymmetric():
    assert generalization_gap(0.7, 0.4) == -generalization_gap(0.4, 0.7)

