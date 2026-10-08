"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/11-deep-infomax/02-softplus/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dim-softplus")
softplus = _module.softplus


import math

import numpy as np


def test_1_softplus_of_zero_is_log_two():
    assert abs(float(softplus(0.0)) - math.log(2.0)) < 1e-12


def test_2_large_inputs_are_nearly_linear():
    assert abs(float(softplus(50.0)) - 50.0) < 1e-9


def test_3_very_negative_inputs_are_nearly_zero():
    assert float(softplus(-50.0)) < 1e-20


def test_4_is_increasing():
    out = softplus(np.array([-1.0, 0.0, 1.0]))
    assert np.all(np.diff(out) > 0)


def test_5_works_on_arrays():
    assert softplus(np.zeros((2, 3))).shape == (2, 3)


def test_6_matches_direct_formula_for_moderate_values():
    x = 0.7
    assert abs(float(softplus(x)) - math.log(1 + math.exp(x))) < 1e-12

