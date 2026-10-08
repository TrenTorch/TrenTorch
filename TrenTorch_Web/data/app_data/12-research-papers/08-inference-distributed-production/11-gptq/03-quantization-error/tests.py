"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/11-gptq/03-quantization-error/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gptq-error")
quantization_error = _module.quantization_error


import numpy as np


def test_1_exactly_representable_values_have_zero_error():
    assert abs(quantization_error(np.array([1.0, -1.0]), 2)) < 1e-12


def test_2_hand_value_with_two_bits():
    # scale 1, codes [1, 0] -> errors [0, 0.4] -> mean 0.2
    assert abs(quantization_error(np.array([1.0, 0.4]), 2) - 0.2) < 1e-12


def test_3_more_bits_reduce_the_error():
    x = np.array([0.31, -0.72, 0.5, 0.11])
    assert quantization_error(x, 8) < quantization_error(x, 3)


def test_4_error_is_nonnegative():
    assert quantization_error(np.array([0.2, -0.9]), 4) >= 0.0


def test_5_returns_a_float():
    assert isinstance(quantization_error(np.array([0.5]), 4), float)


def test_6_zero_weights_have_zero_error():
    assert quantization_error(np.zeros(4), 4) == 0.0

