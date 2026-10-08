"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/11-gptq/01-quantize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gptq-quantize")
quantize_symmetric = _module.quantize_symmetric


import numpy as np


def test_1_largest_magnitude_maps_to_qmax():
    q, _ = quantize_symmetric(np.array([1.0, -1.0, 0.5]), 8)
    assert q[0] == 127 and q[1] == -127


def test_2_all_zeros_quantize_to_zeros():
    q, scale = quantize_symmetric(np.zeros(3), 4)
    np.testing.assert_array_equal(q, [0, 0, 0])
    assert scale == 1.0


def test_3_two_bit_codes_use_range_minus_one_to_one():
    q, _ = quantize_symmetric(np.array([1.0, 0.4]), 2)
    np.testing.assert_array_equal(q, [1, 0])


def test_4_codes_stay_inside_the_range():
    q, _ = quantize_symmetric(np.array([10.0, -10.0, 3.0]), 4)
    assert q.max() <= 7 and q.min() >= -7


def test_5_returns_a_float_scale():
    _, scale = quantize_symmetric(np.array([2.0]), 8)
    assert isinstance(scale, float)


def test_6_does_not_mutate_input():
    x = np.array([1.0, 2.0])
    quantize_symmetric(x, 8)
    np.testing.assert_array_equal(x, [1.0, 2.0])

