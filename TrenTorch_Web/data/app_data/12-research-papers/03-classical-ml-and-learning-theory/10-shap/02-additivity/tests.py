"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/10-shap/02-additivity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shap-additivity")
additivity_gap = _module.additivity_gap


import numpy as np


def test_1_exact_attributions_have_zero_gap():
    assert abs(additivity_gap(np.array([2.0, 3.0]), 10.0, 5.0)) < 1e-12


def test_2_wrong_attributions_give_nonzero_gap():
    assert abs(additivity_gap(np.array([1.0, 1.0]), 10.0, 5.0)) > 1.0


def test_3_sign_shows_which_way_attributions_fall_short():
    assert additivity_gap(np.array([0.0]), 4.0, 1.0) < 0


def test_4_returns_a_python_float():
    assert isinstance(additivity_gap(np.array([1.0]), 2.0, 1.0), float)


def test_5_zero_attributions_match_zero_difference():
    assert additivity_gap(np.zeros(3), 2.0, 2.0) == 0.0


def test_6_works_on_arrays_of_any_length():
    assert additivity_gap(np.ones(10), 12.0, 2.0) == 0.0

