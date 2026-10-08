"""
pytest data/app_data/12-research-papers/01-optimization-and-training/09-large-minibatch/03-worker-count/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-goyal-worker-count")
workers_for_batch = _module.workers_for_batch


import math


def test_1_hand_case():
    assert workers_for_batch(8192, 256) == 32


def test_2_exact_division():
    assert workers_for_batch(1024, 256) == 4


def test_3_partial_worker_is_counted():
    assert workers_for_batch(1000, 256) == 4


def test_4_single_worker_covers_small_batch():
    assert workers_for_batch(10, 256) == 1


def test_5_returns_an_integer():
    assert isinstance(workers_for_batch(100, 7), int)


def test_6_matches_math_ceil():
    assert workers_for_batch(77, 8) == math.ceil(77 / 8)

