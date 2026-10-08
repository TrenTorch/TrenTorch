"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/11-gptq/02-dequantize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gptq-dequantize")
dequantize = _module.dequantize


import numpy as np


def test_1_codes_times_scale():
    np.testing.assert_allclose(dequantize(np.array([2, -1]), 0.5), [1.0, -0.5])


def test_2_zero_codes_give_zero():
    np.testing.assert_allclose(dequantize(np.zeros(3, dtype=int), 9.0), 0.0)


def test_3_unit_scale_returns_codes_as_floats():
    out = dequantize(np.array([3]), 1.0)
    assert out.dtype.kind == "f" and out[0] == 3.0


def test_4_keeps_the_shape():
    assert dequantize(np.ones((2, 3), dtype=int), 2.0).shape == (2, 3)


def test_5_round_trip_is_close_to_original():
    x = np.array([0.9, -0.4, 0.1])
    s = np.max(np.abs(x)) / 127
    q = np.round(x / s).astype(int)
    assert np.max(np.abs(dequantize(q, s) - x)) <= s / 2 + 1e-12


def test_6_does_not_mutate_codes():
    q = np.array([1, 2])
    dequantize(q, 2.0)
    np.testing.assert_array_equal(q, [1, 2])

