"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/09-cpc/03-mi-bound/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cpc-mi-bound")
mi_lower_bound = _module.mi_lower_bound


import math


def test_1_loss_equal_to_log_n_gives_zero_bound():
    assert abs(mi_lower_bound(8, math.log(8.0))) < 1e-12


def test_2_zero_loss_gives_the_maximum_log_n():
    assert abs(mi_lower_bound(4, 0.0) - math.log(4.0)) < 1e-12


def test_3_higher_loss_gives_lower_bound():
    assert mi_lower_bound(10, 2.0) < mi_lower_bound(10, 1.0)


def test_4_returns_a_python_float():
    assert isinstance(mi_lower_bound(3, 0.5), float)


def test_5_more_candidates_raise_the_bound():
    assert mi_lower_bound(100, 1.0) > mi_lower_bound(10, 1.0)


def test_6_bound_is_nonnegative_when_loss_is_at_most_log_n():
    assert mi_lower_bound(16, math.log(16.0) - 0.3) >= 0

