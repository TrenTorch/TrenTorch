"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/07-wavenet/03-mu-law-decode/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-wavenet-mu-law-decode")
mu_law_decode = _module.mu_law_decode


def test_1_zero_maps_to_zero():
    assert abs(float(mu_law_decode(0.0))) < 1e-12


def test_2_one_maps_back_to_one():
    assert abs(float(mu_law_decode(1.0)) - 1.0) < 1e-12


def test_3_round_trip_recovers_the_signal():
    x = np.array([-0.9, -0.1, 0.0, 0.3, 0.8])
    enc = np.sign(x) * np.log1p(255 * np.abs(x)) / np.log1p(255)
    np.testing.assert_allclose(mu_law_decode(enc), x, atol=1e-9)


def test_4_is_odd():
    assert abs(float(mu_law_decode(-0.5)) + float(mu_law_decode(0.5))) < 1e-12


def test_5_is_monotone_increasing():
    out = mu_law_decode(np.linspace(-1, 1, 21))
    assert np.all(np.diff(out) > 0)


def test_6_keeps_the_shape():
    assert mu_law_decode(np.zeros((3, 2))).shape == (3, 2)

