"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/01-rnn-regularization/01-perplexity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zaremba-perplexity")
perplexity = _module.perplexity


import math


def test_1_zero_loss_gives_perplexity_one():
    assert abs(perplexity(0.0, 5) - 1.0) < 1e-12


def test_2_uniform_over_two_symbols_gives_two():
    assert abs(perplexity(3 * math.log(2.0), 3) - 2.0) < 1e-12


def test_3_higher_loss_gives_higher_perplexity():
    assert perplexity(4.0, 2) > perplexity(2.0, 2)


def test_4_returns_a_python_float():
    assert isinstance(perplexity(1.0, 1), float)


def test_5_average_not_total_matters():
    assert abs(perplexity(10.0, 5) - perplexity(20.0, 10)) < 1e-12


def test_6_is_always_at_least_one():
    assert perplexity(0.7, 3) >= 1.0

