"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/07-wavenet/02-mu-law-encode/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-wavenet-mu-law-encode")
mu_law_encode = _module.mu_law_encode


import numpy as np


def test_1_zero_maps_to_zero():
    assert abs(float(mu_law_encode(0.0))) < 1e-12


def test_2_one_maps_to_one():
    assert abs(float(mu_law_encode(1.0)) - 1.0) < 1e-12


def test_3_is_odd():
    assert abs(float(mu_law_encode(-0.4)) + float(mu_law_encode(0.4))) < 1e-12


def test_4_is_monotone_increasing():
    out = mu_law_encode(np.linspace(-1, 1, 21))
    assert np.all(np.diff(out) > 0)


def test_5_small_values_are_expanded_relative_to_linear():
    assert float(mu_law_encode(0.01)) > 0.01


def test_6_keeps_the_shape():
    assert mu_law_encode(np.zeros((2, 3))).shape == (2, 3)

