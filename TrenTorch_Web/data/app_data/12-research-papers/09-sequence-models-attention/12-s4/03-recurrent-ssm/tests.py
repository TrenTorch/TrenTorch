"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/12-s4/03-recurrent-ssm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-s4-recurrent-ssm")
recurrent_ssm = _module.recurrent_ssm


from math import isclose


def ssm_kernel(A_bar, B_bar, C, L):
    return [C * (A_bar**k) * B_bar for k in range(L)]


def causal_conv_from_kernel(K, x):
    T = len(x)
    return [sum(K[k] * x[t - k] for k in range(min(t, len(K) - 1) + 1)) for t in range(T)]


def test_1_matches_the_convolution_form():
    A, B, C = 0.6, 1.2, 0.8
    x = [1.0, -0.5, 2.0, 0.3]
    rec = recurrent_ssm(A, B, C, x)
    conv = causal_conv_from_kernel(ssm_kernel(A, B, C, len(x)), x)
    assert all(isclose(a, b, rel_tol=1e-12, abs_tol=1e-12) for a, b in zip(rec, conv))


def test_2_single_step_is_c_times_b_times_input():
    assert abs(recurrent_ssm(0.5, 2.0, 3.0, [1.0])[0] - 6.0) < 1e-12


def test_3_zero_input_gives_zero_output():
    assert recurrent_ssm(0.5, 1.0, 1.0, [0.0, 0.0]) == [0.0, 0.0]


def test_4_output_length_matches_input():
    assert len(recurrent_ssm(0.9, 0.1, 1.0, [1.0] * 5)) == 5


def test_5_state_carries_over():
    out = recurrent_ssm(1.0, 1.0, 1.0, [1.0, 0.0])
    assert abs(out[1] - 1.0) < 1e-12


def test_6_does_not_mutate_input():
    x = [1.0, 2.0]
    recurrent_ssm(0.5, 0.5, 0.5, x)
    assert x == [1.0, 2.0]

