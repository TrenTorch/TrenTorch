"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/07-deep-double-descent/03-regime/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-double-descent-regime")
double_descent_regime = _module.double_descent_regime


def test_1_fewer_parameters_than_samples_is_underparameterized():
    assert double_descent_regime(10, 3) == "underparameterized"


def test_2_equal_counts_is_the_interpolation_threshold():
    assert double_descent_regime(5, 5) == "interpolation"


def test_3_more_parameters_than_samples_is_overparameterized():
    assert double_descent_regime(4, 100) == "overparameterized"


def test_4_returns_a_string():
    assert isinstance(double_descent_regime(1, 2), str)


def test_5_boundary_is_strict_on_the_underparameterized_side():
    assert double_descent_regime(3, 2) == "underparameterized"


def test_6_one_extra_parameter_crosses_into_overparameterized():
    assert double_descent_regime(7, 8) == "overparameterized"

